from scapy.all import *

from lib.cmd_tool import *

NAME = 'DnsQuery'

class Module:
    def __init__(self):
        self.config = {

        }

        self.help = ''

    def interactive(self):
        interactive(self, 'dns_query')

    def run(self):
        def dns_query():
            pass

        try:
            pass
        except Exception as ex:
            cp.pf_failed(str(ex))