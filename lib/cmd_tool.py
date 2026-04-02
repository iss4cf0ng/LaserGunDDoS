from tabulate import tabulate
from datetime import datetime

import lib.ColorPrint as cp
from lib.EZData import *
from lib.constant import *

def is_quit(cmd: str):
    ls = ['quit', 'q', 'exit']

    return cmd.lower() in ls

def interactive(self, prompt=''):
    while True:
        try:
            cmd = input(f'{prompt}/> ').lower().replace('  ', ' ').split(' ')
            if len(cmd) == 0:
                continue

            if is_quit(cmd[0]):
                break

            if cmd[0] == 'show':
                if len(cmd) > 1:
                    for field in cmd[1:]:
                        show_option(self.config, field)
                    continue

                show_config(self.config)
            elif cmd[0] == 'set':
                if len(cmd) < 3:
                    cp.pf_failed('Usage: set key value')
                    continue

                self.config = set_value(self.config, cmd[1], ','.join(cmd[2:]))
            elif cmd[0] == 'help':
                print(f'\n{self.help}\n')
            elif cmd[0] == 'run':
                if self.validate():
                    self.run()
            else:
                cp.pf_failed('Cannot find command: ' + cmd[0])

        except KeyboardInterrupt:
            print()
            break

def config_console():
    while True:
        pass

def show_config(config: dict):

    lsCol = ['Field', 'Value', 'Description']
    lsRow = list()

    for key in config.keys():
        x = config[key]
        val = x['value']
        msgHelp = x['help']

        msgVal = ''
        if type(val) == list:
            msgVal = ','.join(val)
        else:
            msgVal = str(val)
        if len(msgVal) > 30:
            msgVal = '(...)'

        lsRow.append([key, msgVal, msgHelp])

    print(f'\n{tabulate(lsRow, headers=lsCol)}\n')

def show_val(config: dict, szKey: str):
    val = get_value(config, szKey)
    if not val:
        cp.pf_failed('Value is null or empty.')
        return
    
    lsCol = ['Field', 'Value']
    
    print(f'\n{tabulate([szKey, val], headers=lsCol)}\n')

def check_key(config: dict, szName: str) -> str:
    for key in config.keys():
        if key.lower() == szName.lower():
            return key
        
    return None

def show_option(config: dict, szName: str):
    tmpName = szName
    szName = check_key(config, szName)

    if not szName:
        cp.pf_failed('Cannot find field: ' + tmpName)
        return
    
    if 'options' not in config[szName]:
        show_val(config, szName)
        return

    lsCol = ['Index', 'Description']
    lsRow = list()
    for key in config[szName]['option'].keys():
        lsRow.append([str(key), config[szName]['option'][key]])
    
    print(f'\n{tabulate(lsRow, headers=lsCol)}\n')

def set_value(config: dict, szKey: str, szVal: str) -> dict:
    szValidKey = check_key(config, szKey)
    if not szValidKey:
        cp.pf_failed('Cannot find key: ' + szKey)
        return
    
    config[szValidKey]['value'] = szVal
        
    return config

def get_value(config: dict, szKey: str) -> str:
    szKey = check_key(config, szKey)
    if not szKey:
        return None

    return config[szKey]['value']

def get_help(config: dict, szKey: str) -> str:
    szKey = check_key(config, szKey)
    if not szKey:
        return None

    if 'help' not in config[szKey].keys():
        return None

    return config[szKey]['help']

def get_optionIdx(config: dict, szKey: str) -> int:
    szKey = check_key(config, szKey)
    if not szKey:
        return None
    
    if 'option' not in config[szKey].keys():
        return None
    
    val = config[szKey]['value']
    if not val.isdigit():
        return False

    return int(val)

def set_optionIdx(config: dict, szKey: str, szVal: str) -> bool:
    szKey = check_key(config, szKey)
    if not szKey:
        return False
    
    if 'option' not in config[szKey].keys():
        return False
    
    config[szKey]['option']['value'] = szVal

    return True

def enter_YesNo(prompt='', bDefaultYes = True) -> bool:
    prompt = prompt + ('[Y/n]' if bDefaultYes else '[y/N]')
    cp.pf_quest(prompt)
    
    ans = input('').lower()
    if bDefaultYes and (ans == '' or ans == 'y'):
        return True
    elif not bDefaultYes and (ans == '' or ans == 'n'):
        return True
    else:
        return False
    
def isNonPositiveInt(szInt: str) -> bool:
    return szInt and szInt.isdigit() and int(szInt) > 0
    
def doWorkWithSeconds(work: object, nSecond: int, dicParams: dict) -> int:
    dtStart = datetime.now()

    total = 0

    while (datetime.now() - dtStart).seconds < nSecond:
        left = nSecond - (datetime.now() - dtStart).seconds

        work(**dicParams)
        total += 1
        print(f'Left: {left} (s)\t\t\t', end='\r')
    
    print('\t' * 5)
    
    return total