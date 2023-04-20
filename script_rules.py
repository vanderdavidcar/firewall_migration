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

customer = '1000090BRAEMPU001_'
cmd = net_connect.send_command(f'show run access-list | in {customer}')
print(cmd)

untrustintf = 'UNTRUST-DCV (DCV-1/39.1505)'
"""
Creation rules UNTRUST
"""
# Create Policy objects 

"""
Regex pattern to find exatly subnets
"""
# Pattern to find only access-list IP
pattern_any = re.compile(r"access-list (?P<name_rule>\S+) (?=.*\bpermit\b).+ip (?P<srcaddr>\S+) object-group (?P<dstaddr>\S+)")
pattern_objgr = re.compile(r"access-list (?P<name_rule>\S+) (?=.*\bpermit\b).+ip object-group (?P<srcaddr>\S+) object-group (?P<dstaddr>\S+)")
pattern_obj = re.compile(r"access-list (?P<name_rule>\S+) (?=.*\bpermit\b).+ip object (?P<srcaddr>\S+.) object (?P<dstaddr>\S+.)")
pattern_stand = re.compile(r"access-list (?P<name_rule>\S+) (?=.*\bstandard\b).+permit (\d[0-9].*)")
pattern_anyany = re.compile(r"access-list (?P<name_rule>\S+) (?=.*\bpermit\b).+ip (?P<srcaddr>\S+) (?P<dstaddr>\S+)")

nmmatch_any = re.findall(pattern_any, cmd)
nmmatch_anyany = re.findall(pattern_anyany, cmd)
nmmatch_objgr = re.findall(pattern_objgr, cmd)
nmmatch_obj = re.findall(pattern_obj, cmd)
nmmatch_stand = re.findall(pattern_stand, cmd)
    
# Creating Access-list extended IP
def ip_access_list():
    for i in nmmatch_any:
        if i in nmmatch_any:
            print('edit 0')
            print(f'set name "{i[0]}"')
            print('set srcintf "DCV"')
            print(f'set dstintf "{untrustintf}"')
            if "any" in i[1]:
                print(f'set srcaddr "all"')
            else:
                print(f'set srcaddr "{i[1]}"')
            print(f'set dstaddr "{i[2]}"')
            print('set action accept')
            print('set schedule "always"')
            print('set service "ALL"')
            print('set fsso disable')
            print('next')
    for i in nmmatch_anyany:
        if i in nmmatch_anyany:
            print('edit 0')
            print(f'set name "{i[0]}"')
            print('set srcintf "DCV"')
            print(f'set dstintf "{untrustintf}"')
            if "any" in i[1]:
                print(f'set srcaddr "all"')
            else:
                print(f'set srcaddr "{i[1]}"')
            if "any" in i[2]:
                print(f'set dstaddr "all"')
            else:
                print(f'set dstaddr "{i[2]}"')
            print('set action accept')
            print('set schedule "always"')
            print('set service "ALL"')
            print('set fsso disable')
            print('next')
    for i in nmmatch_objgr:
        print('edit 0')
        print(f'set name "{i[0]}"')
        print('set srcintf "DCV"')
        print(f'set dstintf "{untrustintf}"')
        if "any" in i[1]:
            print(f'set srcaddr "all"')
        else:
            print(f'set srcaddr "{i[1]}"')
        print(f'set dstaddr "{i[2]}"')
        print('set action accept')
        print('set schedule "always"')
        print('set service "ALL"')
        print('set fsso disable')
        print('next')
    for i in nmmatch_obj:
        print('edit 0')
        print(f'set name "{i[0]}"')
        print('set srcintf "DCV"')
        print(f'set dstintf "{untrustintf}"')
        if "any" in i[1]:
            print(f'set srcaddr "all"')
        else:
            print(f'set srcaddr "{i[2]}"')
        print(f'set dstaddr "{i[4]}"')
        print('set action accept')
        print('set schedule "always"')
        print('set service "ALL"')
        print('set fsso disable')
        print('next')
    for i in nmmatch_stand:
        print('edit 0')
        print(f'set name "{i[0]}"')
        print('set srcintf "DCV"')
        print(f'set dstintf "{untrustintf}"')
        print(f'set srcaddr "{i[1]}"')
        print(f'set dstaddr "all"')
        print('set action accept')
        print('set schedule "always"')
        print('set service "ALL"')
        print('set fsso disable')
        print('next')
ip_access_list()

# Pattern to find only access-list TCP
pattern = re.compile(r"access-list (?P<name_rule>\S+)(?=.*\bpermit\b).+tcp")
match = pattern.search(cmd)
name_rule = match.group("name_rule")

dst_pattern = re.compile(r"access-list .+tcp (?P<svc>\w+) object-group (?P<src>\S+) object-group (?P<dst>\S+)")
match = dst_pattern.search(cmd)
svc = match.group("svc")
src = match.group("src")
dst = match.group("dst")
match = re.findall(pattern, cmd)

def tcp_access_list():
    # Creating Access-list extended TCP 
    for i in match:
        print('edit 0')
        print(f'set name "{name_rule}"')
        print('set srcintf "DCV"')
        print(f'set dstintf "{untrustintf}"')
        if "any" in src:
            print(f'set srcaddr "all"')
        else:
            print(f'set srcaddr "{src}"')
        print(f'set dstaddr "{dst}"')
        print('set action accept')
        print('set schedule "always"')
        
        if "any" in svc:
            print(f'set service "all"')
        else:
            print(f'set service "{svc}"')
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
        print('set srcintf "DCV"')
        print(f'set dstintf "{untrustintf}"')
        if "any" or "any4" in srcaddr:
            print(f'set srcaddr "all"')
        else: 
            print(f'set srcaddr "{srcaddr}"')
        print(f'set dstaddr "{dstaddr}"')
        print('set action deny')
        print('set schedule "always"')
        print(f'set service "{svc}"')
        print('set fsso disable')
        print('next')
    print('end')
deny_access_list()