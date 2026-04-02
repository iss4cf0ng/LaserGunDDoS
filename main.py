'''
Project: LaserGunDDoS
Author: iss4cf0ng/ISSAC
'''

import sys

print('Loading...')

from scapy.all import *
from lib import interactive

intro = '''
LaserGUN DoS (Denial of Service)
Author: iss4cf0ng/iss4cf0ng
Github: https://github.com/iss4cf0ng/LaserGunDDoS/

This is a toolkit of denial of service.
You can implement your own tool and put into ./module
'''

def main():
    try:
        iface = sys.argv[1]
        print(iface)
        conf.iface = 'Wi-Fi'

        print(intro)
        interactive.do_interactive()
    
    except Exception as ex:
        print(str(ex))

if __name__ == '__main__':
    main()