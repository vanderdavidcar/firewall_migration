from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

start_time = datetime.now()

"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable()
cmd = net_connect.send_command(f'show run access-list | in INBURSA')
print(cmd)
rules = cmd.splitlines()

untrustintf = 'UNTRUST-DCV (DCV-1/39.1505)'
"""
Creation rules UNTRUST
"""
# Create Policy objects 
print('config firewall policy')
for i in rules:
    """
    Regex pattern to find exatly subnets
    """
    # Pattern to find only static routes on routing table 
    pattern = re.compile(r"access-list (?P<name_rule>\S+) extended (?=.*\bpermit\b)(\w+ )(\w+ )(?P<srcaddr>\w+ )(\w+\S+ )(?P<dstaddr>\w+)")
    match = pattern.search(cmd)
    name_rule = match.group("name_rule")
    srcaddr = match.group("srcaddr") 
    dstaddr = match.group("dstaddr") 
    match = re.findall(pattern, cmd)

    if dstaddr in i:
        print('edit 0')
        print(f'set name "{name_rule}"')
        print('set srcintf "TRUST"')
        print(f'set dstintf "{untrustintf}"')
        print(f'set srcaddr "ALL"')
        print(f'set dstaddr "{dstaddr}"')
        print('set action accept')
        print('set schedule "always"')
        print('set service "ALL"')
        print('set fsso disable')
        print('next')
print('end')
