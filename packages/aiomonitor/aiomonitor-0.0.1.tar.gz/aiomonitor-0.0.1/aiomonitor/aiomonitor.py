import asyncio
import logging
import os
import signal
import socket
import threading
from textwrap import wrap

from terminaltables import AsciiTable

from .utils import (_format_stack, cancel_task, task_by_id, console_proxy,
                    init_console_server)

__all__ = ('Monitor',)


log = logging.getLogger(__name__)


MONITOR_HOST = '127.0.0.1'
MONITOR_PORT = 50101
CONSOLE_PORT = 50102


run_coro = asyncio.run_coroutine_threadsafe


class Monitor:
    def __init__(self, loop, *, host=MONITOR_HOST, port=MONITOR_PORT,
                 console_port=CONSOLE_PORT, console_enabled=True):
        self._loop = loop or asyncio.get_event_loop()
        self._host = host
        self._port = port
        self._console_port = console_port
        self._console_enabled = console_enabled

        log.info('Starting aiomonitor at %s:%d', host, port)

        # The monitor launches both a separate thread and helper task
        # that runs inside curio itself to manage cancellation events
        self._ui_thread = threading.Thread(target=self.server, args=(),
                                           daemon=True)
        self._closing = threading.Event()
        self._ui_thread.start()

        # python console
        self._console_future = None
        if self._console_enabled:
            self._console_future = init_console_server(
                self._host, self._console_port, self._loop)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self._closing.set()
        self._ui_thread.join()
        if self._console_future:
            self._console_future.result(timeout=5)

    def server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass

        # set the timeout to prevent the server loop from
        # blocking indefinitaly on sock.accept()
        sock.settimeout(0.5)
        sock.bind((self._host, self._port))
        sock.listen(1)
        with sock:
            while not self._closing.is_set():
                try:
                    client, addr = sock.accept()
                    with client:
                        sout = client.makefile('w', encoding='utf-8')
                        sin = client.makefile('r', encoding='utf-8')
                        self.interactive_loop(sout, sin)
                except (socket.timeout, OSError):
                    continue

    def monitor_commans(self, sin, sout, resp):
        if not resp or resp.startswith(('q', 'exit')):
            self.command_exit(sout)
            return

        elif resp.startswith('p'):
            self.command_ps(sout)

        elif resp.startswith('cancel'):
            _, taskid_s = resp.split()
            self.command_cancel(sout, int(taskid_s))

        elif resp.startswith('signal'):
            _, signame = resp.split()
            self.command_signal(sout, signame)

        elif resp.startswith('w'):
            _, taskid_s = resp.split()
            self.command_where(sout, int(taskid_s))

        elif resp.startswith('h'):
            self.command_help(sout)

        elif resp.startswith('console'):
            self.command_console(sin, sout)

        else:
            sout.write('Unknown command. Type help.\n')

    def interactive_loop(self, sout, sin):
        """Main interactive loop of the monitor
        """
        (sout.write('\nAsyncio Monitor: %d tasks running\n' %
                    len(asyncio.Task.all_tasks(loop=self._loop))))
        sout.write('Type help for commands\n')
        while not self._closing.is_set():
            sout.write('monitor >>> ')
            sout.flush()
            try:
                resp = sin.readline()
                self.monitor_commans(sin, sout, resp)
            except Exception as e:
                sout.write('Bad command. %s\n' % e)
                sout.flush()

    def command_help(self, sout):
        sout.write(
         '''Commands:
             ps               : Show task table
             where taskid     : Show stack frames for a task
             cancel taskid    : Cancel an indicated task
             signal signame   : Send a Unix signal
             quit             : Leave the monitor
            ''')
        sout.write('\n')

    def command_ps(self, sout):
        headers = ('Task', 'State', 'Task')
        table_data = [headers]
        for task in sorted(asyncio.Task.all_tasks(loop=self._loop), key=id):
            taskid = id(task)
            if task:
                t = '\n'.join(wrap(str(task), 80))
                table_data.append((taskid, task._state, t))
        table = AsciiTable(table_data)
        sout.write(table.table)
        sout.write('\n')
        sout.flush()

    def command_where(self, sout, taskid):
        task = task_by_id(taskid, self._loop)
        if task:
            sout.write(_format_stack(task))
            sout.write('\n')
        else:
            sout.write('No task %d\n' % taskid)

    def command_signal(self, sout, signame):
        if hasattr(signal, signame):
            os.kill(os.getpid(), getattr(signal, signame))
        else:
            sout.write('Unknown signal %s\n' % signame)

    def command_cancel(self, sout, taskid):
        task = task_by_id(taskid, self._loop)
        if task:
            fut = run_coro(cancel_task(task), loop=self._loop)
            # TODO: should we guard this with try except
            fut.result(timeout=3)
            sout.write('Cancel task %d\n' % taskid)
        else:
            sout.write('No task %d\n' % taskid)

    def command_exit(self, sout):
        sout.write('Leaving monitor. Hit Ctrl-C to exit\n')
        sout.flush()

    def command_console(self, sin, sout):
        if not self._console_enabled:
            sout.write('Python console disabled for this sessiong\n')
            sout.flush()
        console_proxy(sin, sout, self._host, self._console_port)
