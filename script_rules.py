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
cmd = net_connect.send_command(f'show run access-list | in {customer}')
print(cmd)

untrustintf = 'UNTRUST-1/39.1505)'
"""
Creation rules UNTRUST
"""
# Create Policy objects 
"""
Regex pattern to find exatly subnets
"""
# Pattern to find only access-list IP
pattern = re.compile(r"access-list (?P<name_rule>\S+)(?=.*\bip\b)")
match = pattern.search(cmd)
name_rule = match.group("name_rule")

dst_pattern = re.compile(r"access-list .+ ip .+ (?P<dstaddr>\w+)")
match = dst_pattern.search(cmd)
dstaddr = match.group("dstaddr") 
match = re.findall(pattern, cmd)

# Creating Access-list extended IP
print('config firewall policy')
def ip_access_list():
    for i in match:
        print('edit 0')
        print(f'set name "{name_rule}"')
        print('set srcintf "{customer}"')
        print(f'set dstintf "{untrustintf}"')
        print(f'set srcaddr "ALL"')
        print(f'set dstaddr "{dstaddr}"')
        print('set action accept')
        print('set schedule "always"')
        print('set service "ALL"')
        print('set fsso disable')
        print('next')
ip_access_list()

# Pattern to find only access-list TCP
pattern = re.compile(r"access-list (?P<name_rule>\S+) extended (?=.*\bpermit\b).+tcp")
match = pattern.search(cmd)
name_rule = match.group("name_rule")

dst_pattern = re.compile(r"access-list .+ tcp.(\w+ )(\w+.\w+ )(?P<src>\S+) (\w+.\w+) (?P<dst>\S+)")
match = dst_pattern.search(cmd)
dst = match.group("dst")
match = re.findall(pattern, cmd)

def tcp_access_list():
    # Creating Access-list extended TCP 
    for i in match:
        print('edit 0')
        print(f'set name "{name_rule}"')
        print('set srcintf "{customer}"')
        print(f'set dstintf "{untrustintf}"')
        print(f'set srcaddr "ALL"')
        print(f'set dstaddr "{dst}"')
        print('set action accept')
        print('set schedule "always"')
        print('set service "ALL"')
        print('set fsso disable')
        print('next')
tcp_access_list()
# Pattern to find only access-list DENY
pattern = re.compile(r"access-list (?P<name_rule>\S+).+ deny")
match = pattern.search(cmd)
name_rule = match.group("name_rule")

serv_pattern = re.compile(r"access-list .+ deny (\w+.\w+) (?P<service>\S+) (?P<srcaddr>\S+) (\w+.\w+) (?P<dstaddr>\S+)")
match = serv_pattern.search(cmd)
svc = match.group("service")
srcaddr = match.group("srcaddr")
dstaddr = match.group("dstaddr")
match = re.findall(pattern, cmd)

def deny_access_list():
    # Creating Access-list extended DENY 
    for i in match:
        print('edit 0')
        print(f'set name "{name_rule}"')
        print('set srcintf "{customer}"')
        print(f'set dstintf "{untrustintf}"')
        print(f'set srcaddr "all"')
        print(f'set dstaddr "{dstaddr}"')
        print('set action deny')
        print('set schedule "always"')
        print(f'set service "{svc}"')
        print('set fsso disable')
        print('next')
    print('end')
deny_access_list()