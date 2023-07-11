import os
import json


class System:
    def uptime(self):
        return os.popen("uptime -p").read().strip()

    def cpu_temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return float(f.read()) / 1000

    def cpu_frequency(self):
        with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as f:
            return float(f.read()) / 1000

    def mem_usage(self):
        return float(os.popen("free -m | awk '/Mem:/ { total=$2 ; used=$3 } END { print used/total*100}'").read().strip())

    def interfaces(self):
        interfaces = os.popen("ls /sys/class/net | grep -v lo").read().split()

        return json.dumps(interfaces)
