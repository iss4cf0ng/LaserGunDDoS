
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def pf_ok(msg):
    print(f'{OKGREEN}[+]{ENDC} {msg}')

def pf_info(msg):
    print(f'{OKBLUE}[*]{ENDC} {msg}')

def pf_failed(msg):
    print(f'{FAIL}[-]{ENDC} {msg}')

def pf_warn(msg):
    print(f'{WARNING}[!]{ENDC} {msg}')

def pf_quest(msg):
    print(f'{BOLD}[?]{ENDC} {msg}')