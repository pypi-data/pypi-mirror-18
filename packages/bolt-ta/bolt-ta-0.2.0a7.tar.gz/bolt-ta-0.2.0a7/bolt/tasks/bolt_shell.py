"""
shell
-----

The ``shell`` task allows executing a shell command with specified arguments
inside the bolt execution context. This task comes handy when no bolt
specific implementation has been provided for a particular task or to invoke
an existing script that should be included as part of the process. 

The trade-off of using this task is that commands are system specific and
it makes it harder to implement a cross-platform ``boltfile.py``.

The task takes a ``command`` parameter specifying the command to be executed,
and an ``arguments`` option that must be set to a list of string for each of
the command line argument tokens to be passed to the tool.

The following example shows how to invoke an existing |python|_ script that
takes a few parameters::

    config = {
        'shell': {
            'command': 'python',
            'arguments': ['existing_script.py', '--with-argument', '-f', '--arg-with', 'a_value']
        }
    }

..  todo::  Find a better example.
"""
import logging
import subprocess as sp

from bolt._bterror import InvalidConfigurationError


class ShellExecuteTask(object):
    
    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self._verify_valid_configuration()
        self._build_command_line()
        return self._run()


    def _verify_valid_configuration(self):
        if not self.config:
            raise InvalidConfigurationError('A shell command is required')
        self.command = self.config.get('command')
        if not self.command:
            raise InvalidConfigurationError('A command must be specified')


    def _build_command_line(self):
        self.command_line = [self.command]
        arguments = self.config.get('arguments')
        if arguments:
            self.command_line.extend(arguments)


    def _run(self):
        logging.debug('Shell command line: ', repr(self.command_line))
        return sp.call(self.command_line)
        


def register_tasks(registry):
    registry.register_task('shell', ShellExecuteTask())
