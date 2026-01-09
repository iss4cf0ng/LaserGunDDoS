from tabulate import tabulate
import os

from lib.cmd_tool import *

g_dicModule = dict()

def init():
    for file in os.scandir('module'):
        if file.name == '__pycache__':
            continue

        file_split = file.name.split('.')
        if file_split[-1].lower() == 'py':
            module_name = '.'.join(file_split[0:(len(file_split) - 1)])
            pattern_module = f'module.{module_name}'
            module = __import__(pattern_module)
            main_module = getattr(module, module_name)

            name = getattr(main_module, 'NAME')

            g_dicModule[name] = main_module

def call_module(module_name: str):
    module = getattr(g_dicModule[module_name], 'Module')

    module().interactive()

def show_module():
    lsName = [_ for _ in g_dicModule.keys()]
    cp.pf_info('Available module:')
    for i in range(0, len(lsName)):
        print(f'\t=> [{i}]: {lsName[i]}')

def do_interactive():
    init()

    while True:
        try:
            cmd = input('> ').lower().split(' ')
            if is_quit(cmd[0]):
                break

            if cmd[0] == 'show':
                show_module()
            elif cmd[0] == 'use':
                if len(cmd) == 1:
                    show_module()
                    continue

                if cmd[1].isdigit():
                    lsName = [_ for _ in g_dicModule.keys()]
                    idx = int(cmd[1])
                    if idx >= len(lsName) or idx < 0:
                        cp.pf_failed(f'Index error: {idx}')
                        continue

                    call_module(lsName[idx])
                else:
                    bFound = False
                    for key in g_dicModule.keys():
                        if key.lower() == cmd[1].lower():
                            bFound = True
                            call_module(key)

                    if not bFound:
                        cp.pf_failed('Cannot find module: ' + cmd[1])
            elif cmd[0] == 'find':
                if len(cmd) == 1:
                    print('Usage: find ModuleName')
                    continue

                lsName = [_ for _ in g_dicModule.keys()]
                bFound = False
                for _ in range(0, len(lsName)):
                    if cmd[1].lower() in lsName[_].lower():
                        print(f'\t[{_}]: {lsName[_]} ')
                        bFound = True
                
                if not bFound:
                    cp.pf_failed('Cannot find module: ' + cmd[1])
            else:
                cp.pf_failed('Cannot find command : ' + cmd[0])

        except KeyboardInterrupt:
            print()
            cp.pf_failed('User quit.')
            break