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
show_route = net_connect.send_command(f"show route | in {customer}")
print(f"Routing Table - {customer}\n\n{show_route}")

# Regex pattern to find exatly subnets
route_pattern = re.compile(
    r"S....(?P<route>\S+[0-9].[0-9].[0-9].[0-9].[0-9].[0-9].[0-9].[0-9]).+via (?P<gateway>\d{1,3}.{1,3}.{1,3}.)"
)
match = route_pattern.search(show_route)
route_match = re.findall(route_pattern, show_route)


def create_routing_table():
    print("\nconfig router static")
    for i in route_match:
        # Create objects address group for current route
        print("edit 0")
        print(f"set dst {i[0]}")
        print(f"set gateway {i[1]}")
        print(f'set device "TRUST-{customer}-1/38.123"')
        print("next")
    print("end")


create_routing_table()
