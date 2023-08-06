# -*- coding: utf-8 -*-

import shlex
import subprocess
import sys


class CommandReturnValue:

    def __init__(self, **kwargs):
        self._return_value = kwargs.get('return_value', None)
        self._stdin = kwargs.get('stdin', None)
        self._stdout = kwargs.get('stdout', None)
        self._stderr = kwargs.get('stderr', None)

    def success(self):
        return self._return_value == 0

    def failure(self):
        return self._return_value != 0 or self._stderr is not None

    def return_value(self):
        return self._return_value

    def stdout(self):
        return self._stdout

    def stderr(self):
        return self._stderr

    def output(self):
        stdout = self.stdout()

        if stdout is None:
            stdout = ''

        return stdout


def exec_command(command, **kwargs):
    """
    Executes the given command and send the output to the console

    :param str|list command:

    :kwargs:
        * `shell`  (``bool`` = False) --
        * `stdin`  (``*`` = None)     --
        * `stdout` (``*`` = None)     --
        * `stderr` (``*`` = None)     --

    :return: CommandReturnValue
    """

    shell = kwargs.get('shell', False)
    stdin = kwargs.get('stdin', None)
    stdout = kwargs.get('stdout', None)
    stderr = kwargs.get('stderr', None)

    kwargs.update(shell=shell)
    kwargs.update(stdin=stdin)
    kwargs.update(stdout=stdout)
    kwargs.update(stderr=stderr)

    if not isinstance(command, list):
        command = shlex.split(command)

    return_value = subprocess.call(command, **kwargs)

    return CommandReturnValue(return_value=return_value,
                              stdin=stdin,
                              stdout=stdout,
                              stderr=stderr)


def observe_command(command, **kwargs):
    """
    Executes the given command and captures the output without any output to the console

    :param str|list command:

    :kwargs:
        * `shell`   (``bool`` = False)  --
        * `timeout` (``int`` = 15)      -- Timeout in seconds
        * `stdin`   (``*`` = None)      --
        * `stdout`  (``*`` = None)      --
        * `stderr`  (``*`` = None)      --
        * `cwd`     (``string`` = None) --

    :return: CommandReturnValue
    """

    shell = kwargs.get('shell', False)
    timeout = kwargs.get('timeout', 15)
    stdin = kwargs.get('stdin', subprocess.PIPE)
    stdout = kwargs.get('stdout', subprocess.PIPE)
    stderr = kwargs.get('stderr', subprocess.PIPE)
    cwd = kwargs.get('cwd', None)

    kwargs.update(shell=shell)
    kwargs.update(stdin=stdin)
    kwargs.update(stdout=stdout)
    kwargs.update(stderr=stderr)
    kwargs.update(cwd=cwd)

    if not isinstance(command, list):
        command = shlex.split(command)

    # TODO: implement and process stdin - 1
    proc = subprocess.Popen(command, **kwargs)

    try:
        # only Python versions from 3.3 have the 'timeout' argument
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 3:
            proc_stdout, proc_stderr = proc.communicate(timeout=timeout)

        else:
            proc_stdout, proc_stderr = proc.communicate()

    except subprocess.TimeoutExpired:
        proc.kill()
        proc_stdout, proc_stderr = proc.communicate()

    # TODO: implement and process stdin - 2
    # process stdin
    # try:
    #     _stdin = proc.stdin.read()
    # except IOError:
    #     _stdin = None
    #
    # if not _stdin:
    #     _stdin = None

    # process stdout
    try:
        _stdout = proc_stdout.decode('utf-8')
    except IOError:
        _stdout = None

    if not _stdout:
        _stdout = None

    # process stderr
    try:
        _stderr = proc_stderr.decode('utf-8')
    except IOError:
        _stderr = None

    if not _stderr:
        _stderr = None

    return CommandReturnValue(return_value=proc.returncode,
                              stdout=_stdout,
                              stderr=_stderr)
