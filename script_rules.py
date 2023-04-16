from netmiko import ConnectHandler
import dev_connection
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

start_time = datetime.now()

# prefix group name of object "addgr" to use for loop
objects = ["fontnet", "redes"]

"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable()
cmd = net_connect.send_command(f'show run access-list | in PACI')
print(cmd)

"""
Creation rules UNTRUST
"""
# Create Policy objects 
print('config firewall policy')
for i in objects:
    print('edit 0')
    print('set srcintf "DCV"')
    print(f'set dstintf "{i.upper()}_PACI"')
    print('set srcaddr "all"')
    print(f'set dstaddr "{i.upper()}_PACI"')
    print('set action accept')
    print('set schedule "always"')
    print('set service "ALL"')
    print('set fsso disable')
    print('next')
