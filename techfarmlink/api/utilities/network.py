import os
import re


class Network:
    def interfaces(self):
        cmd = os.popen("ls /sys/class/net | grep -v lo").read()
        net = cmd.strip().split('\n')

        return net

    def dhcp_leases(self):
        cmd = os.popen("dhcp-lease-list --parsable |awk '{ print $2 \"||\" $4 \"||\" $6 \"||\" $8 \" @ \" $9 \"||\" $11 \" @ \" $12}'").read()

        if not cmd:
            return []

        dev = [dict(zip(['mac', 'ip', 'host', 'begin', 'expire'], a.split('||'))) for a in cmd.strip().split('\n')]
        dev = [{k: v.upper() if k == 'mac' else v for k, v in a.items()} for a in dev]

        return dev

    def arp_list(self):
        cmd = os.popen("arp -an|grep -oE '10\.0\.[0-9]{1,3}\.[0-9]{1,3}'").read()
        ips = cmd.strip().split('\n')

        return ips

    @staticmethod
    def device_mac(ip):
        cmd = os.popen(f"arp -an {ip} | grep -o '..:..:..:..:..:..'").read()

        return cmd.upper()
