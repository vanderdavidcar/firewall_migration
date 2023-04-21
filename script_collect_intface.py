#! /usr/bin/env python3

from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

start_time = datetime.now()

customer = "ITAU"
"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable()  # Needed beacause command below is necessary privilege 15 to be executed
term_pager0 = net_connect.send_command("terminal pager 0")
show_intface = net_connect.send_command('show run interface | in Port-channel11.')
iface = show_intface.splitlines()
print(f"Cisco ASA interface- {iface}")


def collect_interfaces():

    print("Fortigate interfaces")
    print("\nconfig system interface")
    for i in iface:
        cmd = net_connect.send_command(f"show run {i}")

        """
        Regex pattern to find exatly subnets
        """
        vlan_pattern = re.compile(r"vlan (?P<vlanid>\S.*)")
        vlan_match = vlan_pattern.search(cmd)
        vlanid = vlan_match.group("vlanid")

        ipaddr_pattern = re.compile(
            r"ip address (?P<ipaddr>\S.+[0-9].[0-9].[0-9].[0-9].[0-9].[0-9].[0-9])"
        )
        ipaddr_match = ipaddr_pattern.search(cmd)
        ipaddr = ipaddr_match.group("ipaddr")
        ipaddr_match = re.findall(ipaddr_pattern, cmd)

        print(f'edit "TRUST-{customer}-1/38.{vlanid}')
        print('set vdom "DCV"')
        print(f'set ip {ipaddr}')
        print('set allowaccess ping')
        print(f'set alias "TRUST-{customer}"')
        print('set device-identification enable')
        print('set role lan')
        print('set interface "port38"')
        print(f'set vlanid {vlanid}')
        print('next')
    print('end')


collect_interfaces()
