from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
import logging

start_time = datetime.now()

"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable() # Needed beacause command below is necessary privilege 15 to be executed
term_pager0 = net_connect.send_command('terminal pager 0')
show1_intface = net_connect.send_command(f'show run interface')
show_intface = net_connect.send_command(f'show run interface | in Port-channel11.')
iface = show_intface.splitlines()
print(f'Cisco ASA - {iface}')

def collect_interfaces():
    print('Fortigate interfaces')
    print('\nconfig system interface')
    for i in iface:
        cmd = net_connect.send_command(f'show run {i}')
    
        """
        Regex pattern to find exatly subnets
        """
        int_pattern = re.compile(r"interface (?P<intface>\S......)")
        int_match = int_pattern.search(cmd)
        intface = int_match.group("intface")
        int_match = re.findall(int_pattern, cmd)

        vlan_pattern = re.compile(r"vlan (?P<vlanid>\S.*)")
        vlan_match = vlan_pattern.search(cmd)
        vlanid = vlan_match.group("vlanid")
        vlanid_match = re.findall(vlan_pattern, cmd)

        nameif_pattern = re.compile(r"nameif (?P<client>\S.*)")
        nameif_match = nameif_pattern.search(cmd)
        client = nameif_match.group("client")
        nameif_match = re.findall(nameif_pattern, cmd)

        ipaddr_pattern = re.compile(r"ip address (?P<ipaddr>\S.+[0-9].[0-9].[0-9].[0-9].[0-9].[0-9].[0-9])")
        ipaddr_match = ipaddr_pattern.search(cmd)
        ipaddr = ipaddr_match.group("ipaddr")
        ipaddr_match = re.findall(ipaddr_pattern, cmd)

        print(f'edit "TRUST-PACI-DCV-1/38.{vlanid}')
        print(f'set vdom "DCV"')
        print(f'set ip {ipaddr}')
        print(f'set allowaccess ping')
        print(f'set alias "TRUST-{client}"')
        print(f'set device-identification enable')
        print(f'set role lan')
        print(f'set interface "port38"')
        print(f'set vlanid {vlanid}')
        print('next')
    print('end')
collect_interfaces()
