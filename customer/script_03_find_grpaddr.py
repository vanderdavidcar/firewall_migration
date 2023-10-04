from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
import os 
import time
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
shrun = net_connect.send_command(f"show running-config | in 198.32.5")

"""
Function to find object-group names used in access-list Internet-ACL to looking for source IPs
"""

def rule_grp_object():
    # Regex Pattern
    object_group = "access-list.*object-group.(\S+)"
    regex_grp = re.findall(object_group, shrun)
    
    cmd = net_connect.send_command(f'show running-config object-group')
    show_objgrp = cmd.splitlines()

    print(f"\nAll object-group find out in ACL named Internet-ACL")
    for grp in regex_grp:
        print(f"\n{grp}")

        # this regex is to match for all object-group on firewall Cisco ASA
        grpname_pattern = "object-group network (?P<grpname>\S+)"
        grpname_regex = re.compile(grpname_pattern)

        netobj_pattern = "network-object host (?P<hosts>\S+)"
        netobj_regex = re.compile(netobj_pattern)

        # Convert address objects in Cisco ASA to Fortigate object group
        for row in show_objgrp:
            # Create objects address group         
            if grpname_regex.search(row):
                grpname = row.split()[2]
            if netobj_regex.search(row):
                netobject = row.split()[2]
                newgrp = []
                newgrp.append(netobject)
                
                
                
                for i in newgrp:
                    if grpname == f"{grp}":
                        ipadd = f'{i}/32'

                        print(i)
                        ip = f"".join(ipadd)
                        new_ips = []
                        new_ips.append(ip)
                        ipaddr = f'{new_ips}'
                        
                        # Create file with IP address in all object-groups
                        with open(f'output_addrgrp_ips.txt', 'a') as f:
                            f.write(f'{i}\n')
                            f.close()
                            
                            # Remove all duplicated IP address
                            del_duplicated = f'sort -u output_addrgrp_ips.txt > output_addrgrp_new_ips.txt'
                            cmdFile = os.system(del_duplicated)
                                                
                        # Create new file with non duplicated IPs
                        if grpname:
                            # Create object group
                            with open(f'retrieve_{grpname}_ips.txt', 'a') as f:
                                f.write(f'{str(ipaddr)}')
                                f.close()

                            # Create object group
                            with open(f'output_{grpname}_ips.txt', 'a') as f:
                                f.write(f'{i}/32\n')
                                f.close()
                                
                            # Remove special characteres to use data on address group
                            delcharctere = f"sed -i 's/\[/ /g' retrieve_{grpname}_ips.txt && sed -i 's/\]//g' retrieve_{grpname}_ips.txt"
                            cmdFile = os.system(delcharctere)
                            time.sleep(0.5)
                        
rule_grp_object()