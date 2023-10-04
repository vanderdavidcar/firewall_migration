from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
import os 
load_dotenv()

start_time = datetime.now()
print(f"{start_time}")

"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable()  # Needed beacause command below is necessary privilege 15 to be executed
term_pager0 = net_connect.send_command("terminal pager 0")

# Command executed on Cisco ASA to find a costumer configuration
shrun = net_connect.send_command(f"show running-config | in 201.31.5")


# Regex pattern
source = "access-list Internet-ACL.*tcp.host.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
src_regex = re.findall(source, shrun)

destination = "access-list Internet-ACL.*host.(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
dst_regex = re.findall(destination, shrun)

"""
Loop to find IP Addresses on access-list extended on Cisco ASA and convert on FortiOS script to create address object prefix-lenght /32 that should be used on rules
"""

def find_addr_object():
    data = ['source', 'destination']

    # Looking for source IP addresses in ACL
    for i in src_regex:

        # Creating a external file 
        with open(f'output_source_ips.txt', 'a') as f:
            f.write(f'{i}\n')
            f.close()

    # Looking for destination IP addresses in ACL
    for i in dst_regex:

        # Creating a external file 
        with open(f'output_destination_ips.txt', 'a') as f:
            f.write(f'{i}\n')
            f.close()

    # Remove all duplicated data in files
    for i in data:
        # Save nmap output file 
        del_duplicated = f'sort -u output_{i}_ips.txt > output_{i}_new_ips.txt'
        cmdFile = os.system(del_duplicated)
find_addr_object()

"""
Creating all IP address objects in external file 
"""

def create_addr_object():
    

    # Used to loop in file name
    ipaddr = ['source','destination', 'addrgrp']
    
    for i in ipaddr:
        # Using external file
        with open(f'output_{i}_new_ips.txt', 'r') as f:
            new_ips = f.read().splitlines()
        
            for line in new_ips:
                print(f'edit {line}/32')
                print(f"set subnet {line} 255.255.255.255")
                print("next")
            print("end")

create_addr_object()
