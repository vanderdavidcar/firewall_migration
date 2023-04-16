from netmiko import ConnectHandler
import dev_connection
import re
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

start_time = datetime.now()

"""
Call function dev_connection that have all device and user information to connect and collect
"""
net_connect = ConnectHandler(**dev_connection.iosv)
net_connect.enable() # Needed beacause command below is necessary privilege 15 to be executed
show_route = net_connect.send_command('show route | in PACI')

def routing_table():
    print(f'Routing Table - PACI\n\n{show_route}')
    """
    Regex pattern to find exatly subnets
    """
    # Pattern to find only static routes on routing table 
    route_pattern = re.compile(r"S....(?P<route>\S+[0-9].[0-9].[0-9].[0-9].[0-9].[0-9].[0-9].[0-9])")
    match = route_pattern.search(show_route)
    dest = match.group("route")
    route_match = re.findall(route_pattern, show_route)

    # Pattern to find gateway of network
    gw_pattern = re.compile(r"S.*(?P<gateway>\S..+[0-9][0-9].[0-9].[0-9])")
    gw_match = gw_pattern.search(show_route)
    gw = gw_match.group("gateway")
    gw_match = re.findall(gw_pattern, show_route)
    
    # Create objects address group
    print('\nconfig router static')
    for i in route_match:
        print('edit 0')
        print(f'set dst {i}')
        print(f'set gateway {gw}')
        print('set device "TRUST-PACI-DCV-1/38.123"')
        print('next')
print('end')
routing_table()