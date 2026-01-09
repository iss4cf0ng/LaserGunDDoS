from scapy.all import *

from lib.cmd_tool import *

NAME = 'DnsAmplification'

class Module:
    def __init__(self):
        self.config = {

        }

        self.help = ''

    def interactive(self):
        interactive(self)

    def run(self):
        try:
            pass
        except Exception as ex:
            cp.pf_failed(str(ex))