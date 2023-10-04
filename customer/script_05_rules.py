from netmiko import ConnectHandler
import dev_connection
import re, os
from dotenv import load_dotenv
from datetime import datetime
import fileinput


load_dotenv()

start_time = datetime.now()

"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable()  # Needed beacause command below is necessary privilege 15 to be executed
term_pager0 = net_connect.send_command("terminal pager 0")


"""
Retrieve all source and destination IP Addresses find out in access-list Internet-ACL 
"""

shrun = net_connect.send_command(f"show running-config | in 198.32.5.")

# Firewall interfaces
intf_untrust = "UNTRUST-39.1527"
intf_trust = "TRUST-1/38.1040"

"""
Function to find object-group names used in access-list Internet-ACL to looking for source IPs
"""

# Regex pattern to find source, destination and ports in access-list
destination = "access-list Internet-ACL.*tcp.host.(\S+).host.(\S+).eq.(\S+)"
dest_regex = re.findall(destination, shrun)

any4 = "access-list Internet-ACL.*tcp.(\S+).host.(\S+).eq.(\S+)"
any4_regex = re.findall(any4, shrun)

object_group = "access-list.*object-group.(\S+).host.(\S+).eq.(\S+)"
regex_grp = re.findall(object_group, shrun)

"""
Function to create rules based on informations outputd above
"""

def create_new_objectgrp():
        for grpobj in regex_grp:
                if regex_grp:

                        ipaddr = ["198.32.5.4", "198.32.5.9"]
                        for ipadd in ipaddr:

                                if  ipadd in grpobj:
                                        tcpports = ['8443','7443','8088']

                                        for i in tcpports:
                                                if grpobj[2] == i:
                                                        with fileinput.input(files=(f'output_{grpobj[0]}_ips.txt')) as f:
                                                                for line in f:

                                                                    with open(f"output_{grpobj[1]}_{grpobj[2]}_newgrpaddr.txt", "a") as f:
                                                                        f.write(line)
                                                                        f.close()

create_new_objectgrp()

def create_rule():
        for grpobj in regex_grp:
                
                # Delete all IP address
                del_duplicated = f'sort -u output_{grpobj[1]}_{grpobj[2]}_newgrpaddr.txt > output_{grpobj[1]}_{grpobj[2]}_ips.txt'
                cmdFile = os.system(del_duplicated)
                
                # Open external file that have the new groups of IP from specific ports '8443','7443','8088' founded in function below
                with open(f"output_{grpobj[1]}_{grpobj[2]}_ips.txt", "r") as f:
                        ip = f.read().splitlines()

                # Create firewall (FortiOS) rule 
                print("edit 0")
                print(f'set name "ALLOWED-to-{grpobj[1]}-TCP/{grpobj[2]}"')
                print(f'set srcintf "{intf_untrust}"')
                print(f'set dstintf "{intf_trust}"')
                print(f'set srcaddr "{ip}"')
                print(f'set dstaddr "{grpobj[1]}/32"')
                print("set action permit")
                print('set schedule "always"')
                print(f'set service "{grpobj[2]}"')
                print("set fsso disable")
                print("next")
create_rule()