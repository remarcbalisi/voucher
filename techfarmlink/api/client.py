import sys
import re
from datetime import datetime

from techfarmlink.api.utilities.iptables import Iptables

ip = sys.argv[1]
mac = sys.argv[2]
host = sys.argv[3]

ipt = Iptables(ip)
ipt.add_client()

# if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
#     mac = ':'.join(map(lambda s: s.zfill(2), mac.split(':')))
#
# if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip) and re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
#     db = Database()
#
#     db.set_ip(ip)
#     db.set_host(host)
#     db.set_mac(mac.upper())
#
#     if not db.get_device_id():
#         db.add_device()
#         sys.exit()
#
#     db.update_device()
#
#     mb_limit, mb_used = db.get_data_usage()
#     time_limit, time_consumed = db.get_time_usage()
#
#     less_than_mb_limit = mb_limit <= mb_used
#     less_than_time_limit = time_limit <= time_consumed
#
#     if not (less_than_mb_limit and less_than_time_limit):
#         ipt = Iptables(ip)
#         ipt.add_client()
#
#         dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         # session[db.get_device_id_by_ip()]['LAST_TIME_IN'] = dt

sys.exit()
