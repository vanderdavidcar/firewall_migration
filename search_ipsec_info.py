from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime

# To have a logging only for Netmiko connection
import logging

"""
Logging is important to troubleshooting code 
"""
logging.basicConfig(filename="netmiko_global.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")


load_dotenv()


"""
Call function dev_connection that have all devices and users information to connect on devices and collect information we need
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable() # privileged EXEC mode
term_pager0 = net_connect.send_command('terminal pager 0') # terminal page to zero (0) removes any output pagination and will return all output from executing the specified command

cmd = net_connect.send_command(f'sh vpn-sessiondb l2l')

# Find Peer IPSec
ipaddr = "Connection.* (\d.*)"
match = re.findall(ipaddr, cmd)


for i in match:
    print(f'Peer: {i}')
    # Use remote peer IPSec to find configuration
    ip = net_connect.send_command(f'sh run | in {i}')

    # Find all information compressed by crypto map and retrieve only the name of map with sequency numnber
    crypto = "crypto map (\S+ \d+)"
    outside_map = re.findall(crypto,ip)

    for i in outside_map:
        if i in outside_map:
            # To find access-list matched with crypt map 
            info_outside_map = net_connect.send_command(f'sh run | in {i} match')
            
            crypto_map = "crypto map.*match address (\S+)"
            outside_cryptomap = re.findall(crypto_map,info_outside_map)
            

        # Find object-group with customer project ID         
        for i in outside_cryptomap:
            info_cryptomap = net_connect.send_command(f'sh run | in {i} extended')
            lines = info_cryptomap.splitlines()
    
        
            acl = "access-list .*object-group (\d+)"
            ac2 = "access-list.*extended permit ip object-group (\S+ )object-group (\S+)"
            projectID = re.findall(acl,info_cryptomap)
            object_group = re.findall(ac2,info_cryptomap)
            print(f'Project ID: {projectID}')
            print(f'Object-group: {object_group}\n')
            

    

