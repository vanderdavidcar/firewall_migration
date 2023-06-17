from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
import csv

load_dotenv()

start_time = datetime.now()

"""
Call function dev_connection that have all devices and users information to connect on devices and collect information we need
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable() # privileged EXEC mode
term_pager0 = net_connect.send_command('terminal pager 0') # terminal page to zero (0) removes any output pagination and will return all output from executing the specified command

# variable to use in cisco commands to show informations
customer = '201.31.0'

cmd = net_connect.send_command(f'show run access-list | in {customer}')
cmd1 = net_connect.send_command(f'show running-config object-group')
cmd2 = net_connect.send_command(f'show running-config nat | in {customer}')

show_objgrp = cmd1.splitlines()
show_nat = cmd2.splitlines()

print('!Access-list configured on Cisco ASA\n')
shrun_rules = cmd.splitlines()

# Pattern to find only IPs started by 201.31.0
pattern_201 = re.compile(r"(?P<ip>201.31.0.[0-9]+)")
match_201 = re.findall(pattern_201, cmd1)

# varibale result to remove all duplicated value found in list
result = []

print('\nList of IPs used to convert from Cisco ASA objects to Fortigate addresses')
for i in match_201:
    if i not in result:
        result.append(i) # creating a new list without duplicated value
print(result) # Find all IP addresses started by 201.31.0 on Cisco Asa to create a address objects.

# Create objects address in Fortigate using data retrieved from Cisco ASA above
print(f'\nconfig firewall address')
def create_subnets():
    for i in result:                    
        print(f'edit "{i}/32"') 
        print(f'set subnet {i} 255.255.255.255')
        print("next")
create_subnets()

# Reading externall file with some IPs to create address object
with open('source_ips.txt', 'r') as f:
    src_ips = f.read().split()

# Function to create addresses objects 
def create_src_hosts():
    for i in src_ips:                    
        print(f'edit "{i}/32"') 
        print(f'set subnet {i} 255.255.255.255')
        print("next")
    print("end\n")
create_src_hosts()

# Service ports need to be created on Fortigate
def create_tcpudp_ports():
    ports = ['9006', '3000', '8280']

    print("\nconfig firewall service custom")
    for tcp in ports:
        print(f"edit {tcp}_TCP")
        print(f"set tcp-portrange {tcp}")
        print(f"set udp-portrange {tcp}")
        print("next")
    print("end\n")
create_tcpudp_ports()

"""
Another method to retrive information using .csv file to create a dicionary on python
"""
def create_rules():
    source_file = "rules.csv"
    
    # Create a dictionary with data retireve from .csv file
    with open(source_file) as f:
         reader = csv.DictReader(f)
         
         # Loop of rules will be created on fortigate according to data retrieved from rule.csv file above
         print('config firewall policy')
         for row in reader:
            print('edit 0')
            print(f'set name "{row["name"]}"')
            print(f'set srcintf "{row["incoming_intf"]}"')
            print(f'set dstintf "{row["outgoing_intf"]}"')
            print(f'set srcaddr "{row["source"]}"')
            print(f'set dstaddr "{row["destination"]}"')
            print('set action accept')
            print('set schedule "always"')
            print(f'set service "{row["service"]}"')
            print('set ssl-ssh-profile "certificate-inspection"')
            print('set ips-sensor "g-default"')
            print('set fsso disable')
            print('next')
    print('end\n')
create_rules()

# Loop of rules will be created on fortigate according to data retrieved from rule.csv file above
def create_object_groups():
    source_file = "rules_gp.csv"
    with open(source_file) as f:
        reader = csv.DictReader(f)
        print('config firewall addrgrp')
        for row in reader:
            print(f'edit "{row["gp_name"]}"')
            print(f'append member {row["members"]}')
            print('next')
    print('end\n')
create_object_groups()
