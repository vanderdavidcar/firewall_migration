#! /usr/bin/env python3
from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
import time, os
load_dotenv()


# To have a logging only for Netmiko connection
import logging

start_time = datetime.now()


"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable()
term_pager0 = net_connect.send_command('terminal pager 0')

# Find all access-list from specific block IP address
showrun = net_connect.send_command(f"show running-config | in 198.32.5")
shrun = str(showrun.splitlines())

any4 = "access-list Internet-ACL.*tcp.(\S+).host.(\S+).eq.(\d+)"
any4_regex = re.findall(any4, showrun)

"""
All TCP ports used on access-list
"""

#This is loop you can use all ports founded on access-lists
#for grpobj in any4_regex:
#        tcp = grpobj[2]
#        print(tcp)
    

def create_tcpudp_ports():
    
    # Specific list ports to use on loop below
    ports = ['7443', '8443', '1935', '1024','9443', '8088', '18090', '18090']

    print("\nconfig firewall service custom")    
    for tcp in ports:
        print(f"edit {tcp}_TCP")
        print(f"set tcp-portrange {tcp}")
        print("next")
    
    # Ports range find out on Cisco ASA
    numbers = range(6880,6930)
    for i in numbers:
        port = f'TCP_{i}'
        print(f"edit {port}")
        print(f"set tcp-portrange {i}")
        #print(f"set udp-portrange {i}")
        print("next")
    

        # Create a service group using ports above

        ip = "".join(str(port))
        new_ips = []
        new_ips.append(ip)
        

        # Create new file with non duplicated IPs
        rng = "portrange"
        with open(f'retrieve_{rng}_ips.txt', 'a') as f:
            f.write(f'{str(new_ips)}')
            f.close()
        
            # Remove special characters to use data on address group using bash command "sed"
            delcharactere = f"sed -i 's/\[/ /g' retrieve_{rng}_ips.txt && sed -i 's/\]//g' retrieve_{rng}_ips.txt"
            cmdFile = os.system(delcharactere)
            time.sleep(0.5)

    # Read a file that have all TCP Ports to create a service group
    with open(f'retrieve_{rng}_ips.txt', 'r') as fa:
        cust_port = fa.read().splitlines()
        print("\nconfig firewall service group")
        print(f'edit "TCP-6880_to_6929"')
        print(f'append member "{cust_port}"') 

create_tcpudp_ports()

end_time = datetime.now()
print(f'Initial time {end_time - start_time}')