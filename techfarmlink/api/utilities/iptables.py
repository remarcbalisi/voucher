import os
import time


class Iptables:
    def __init__(self, ip_addr):
        self.ip = ip_addr

    def add_client(self):
        while not os.popen(f"sudo iptables -t nat -nL PREROUTING | grep -w '{self.ip}'").read():
            os.system(f"sudo iptables -t nat -I PREROUTING -s {self.ip} -j ACCEPT")

        while not os.popen(f"sudo iptables -nL FORWARD | grep -w '{self.ip}'").read():
            os.system(f"sudo iptables -A FORWARD -d {self.ip} -j ACCEPT; sudo iptables -A FORWARD -s {self.ip} -j ACCEPT")
            time.sleep(1)

    def rem_client(self):
        while os.popen(f"sudo iptables -t nat -nL PREROUTING | grep -w '{self.ip}'").read():
            os.system(f"sudo iptables -t nat -D PREROUTING -s {self.ip} -j ACCEPT")
            time.sleep(1)

        while os.popen(f"sudo iptables -nL FORWARD | grep -w '{self.ip}'").read():
            os.system(f"sudo iptables -D FORWARD -s {self.ip} -j ACCEPT; sudo iptables -D FORWARD -d {self.ip} -j ACCEPT")
            time.sleep(1)

    def connected(self):
        if not os.popen(f"sudo iptables -nL FORWARD | grep -w '{self.ip}'").read():
            return False

        return True
