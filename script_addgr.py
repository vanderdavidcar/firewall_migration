#! /usr/bin/env python3

from netmiko import ConnectHandler
from ipaddress import IPv4Network
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


start_time = datetime.now()

# prefix group name of object "addgr" to use for loop
objects = ["fontnet", "redes"]

# Call function dev_connection that have all device and user information to connect and collect
net_connect = ConnectHandler(**dev_connection.iosv)

"""
Lists of IPs took from function "remove_dup_ips.py" on Cisco ASA that remove all duplicate IPs and generete a new file to use here to create the objects in Fortigate.
"""


def create_objects():

    for name in objects:
        if name in objects:
            print(f"\nNetwork Objects {name.upper()}_PACI")
            redes = open(f"{name}_new_ips.txt", "r")
            address = redes.read().split()

        # Creaiton of objects based on IPs list below
        print("\nconfig firewall address")
        for host in address:
            # Command executed on Cisco ASA to find a costumer configuration
            show_run = net_connect.send_command(f"show running-config | in {host}")
            # Regex pattern to find exatly subnets on Cisco ASA
            pattern = re.compile(r"subnet (?P<subnet>\S.+)")
            match = pattern.search(show_run)
            subnet = match.group("subnet")

            """"
            Find subnets and prefix to create object addresses
            """

            # manipulation of variable to put prefix and mask in the correct way and show us subnets matched with regex pattern
            sub_mask = subnet.split()
            sub1_mask = "/".join(sub_mask)
            net = IPv4Network(sub1_mask)
            if f"subnet {host}" in show_run:
                ip_prefix = f"{host}/{net.prefixlen}"
                ip_mask = f"{host} {net.netmask}"
            """
            Scripts to execute on Fortigate to create address and address group
            """
            # Create objects addresses based on subnets found above by regex
            print("edit " + str(ip_prefix))
            print(f"set subnet {ip_mask}")
            print("next")
        print("end")

        # Create objects address group
        print("\nconfig firewall addrgrp")
        b = '" "'.join(address)
        print(f"edit {name}_PACI")
        print(f"set member append {b}\n")

    end_time = datetime.now()
    print("Total time: {}".format(end_time - start_time))


create_objects()
