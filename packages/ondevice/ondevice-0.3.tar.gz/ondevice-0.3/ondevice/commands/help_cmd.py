"""
Lists available commands or prints detailed help for one of them

Examples:
    {cmd} help          lists available commands
    {cmd} help listen   shows the help for the 'listen' command
    {cmd} help help     shows this message
"""

usage = {
    'args': '[cmd]',
    'msg': 'lists available commands or prints detailed help for one'
}

from ondevice import commands
from ondevice.core import exception

import sys

def run(cmdName=None):
    if cmdName == None:
        print("USAGE: {0} <command> [args]\n".format('ondevice'))

        cmds = {'client':[], 'device':[], None:[]}
        groupNames = {'client': 'Client commands', 'device': 'Device commands', None: 'Other commands'}
        for cmd in commands.listCommands():
            usage = commands.usage(cmd)
            usage.setdefault('cmd', cmd)
            usage.setdefault('args', '')
            group = usage.setdefault('group', None)
            hidden = usage.setdefault('hidden', False)

            if group not in cmds.keys():
                group = None
            if not hidden:
                cmds[group].append(usage)

        for group in ['device', 'client', None]:
            print("- {0}:".format(groupNames[group]))
            for usage in cmds[group]:
                print("    {cmd} {args}\n\t{msg}".format(**usage))
            print('')
    else:
        cmd = commands.load(cmdName)

        if not hasattr(cmd, '__doc__') or cmd.__doc__ == None:
            raise exception.ImplementationError("Command '{0}' lacks documentation!".format(cmdName))

        usage = commands.usage(cmdName)
        usage.setdefault('cmd', cmdName)
        usage.setdefault('args', '')
        print('{0} {cmd} {args}'.format('ondevice', **usage))
        print(cmd.__doc__.format(cmd='ondevice'))
