

print('Loading...')

from scapy.all import *
from lib import interactive

intro = '''
LaserGUN DoS (Denial of Service)
Author: iss4cf0ng
Github: 

This is a toolkit of denial of service.
You can implement your own tool and put into ./module
'''

def init():
    conf.iface = 'Wi-Fi'

def main():
    init()

    print(intro)
    interactive.do_interactive()

if __name__ == '__main__':
    main()