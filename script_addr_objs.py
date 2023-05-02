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
net_connect.enable()  # Needed beacause command below is necessary privilege 15 to be executed
term_pager0 = net_connect.send_command("terminal pager 0")
# Command executed on Cisco ASA to find a costumer configuration
show_run = net_connect.send_command(f"show running-config object")
show_services = net_connect.send_command(f"show running-config object | in service")


def create_object_addr():

    # this regex is to match for gigabit, ethernet, fastethernet and loopback.
    obj_pattern = "network (?P<name>\S+)"
    hst_pattern = "host (?P<host>\S+)"
    sub_pattern = "subnet (?P<subnet>\S+)"
    rng_pattern = "range (?P<range>\S.+)"

    # create a regex object with the pattern in place.
    regex_nam = re.compile(obj_pattern)
    regex_hst = re.compile(hst_pattern)
    regex_sub = re.compile(sub_pattern)
    regex_rng = re.compile(rng_pattern)

    # initialize this list to collect interface information.

    print(f"\nconfig firewall address")
    for line in show_run.splitlines():
        # check for interface names only
        if regex_nam.search(line):
            name = line.split()[2]
            print(f"edit {name}")
        if regex_hst.search(line):
            host = line.split()[1]
            print(f"{host}/32")
            print("next")
        if regex_sub.search(line):
            sub = line.split()[1:]
            subnet = " ".join(sub)
            print(subnet)
            print("next")
        if regex_rng.search(line):
            rng = line.split()[1:]
            range = " ".join(rng)
            print(range)
            print("next")
    print("end")


create_object_addr()


def create_services_obj():

    # this regex is to match for all services on firewall Cisco ASA
    srv_pattern = "object service (?P<service>\S+)"
    srv_regex = re.compile(srv_pattern)

    udp_pattern = ".+udp .+eq (?P<udp>\S+)"
    udp_regex = re.compile(udp_pattern)

    tcp_pattern = ".+tcp .+eq (?P<tcp>\S+)"
    tcp_regex = re.compile(tcp_pattern)

    # Convert address objects from Cisco ASA to Fortigate object services
    print("\nconfig firewall service")
    for line in show_services.splitlines():
        if srv_regex.search(line):
            nmservice = line.split()[2]
        if tcp_regex.search(line):
            print(f"edit {nmservice}")
            tcp = line.split()[4]
            if "ldap" in tcp:
                print(f"set tcp-portrange 389")
            else:
                print(f"set tcp-portrange {tcp}")
        if udp_regex.search(line):
            print(f"edit {nmservice}")
            udp = line.split()[4]
            print(f"set udp-portrange {udp}")
            print("next")
    print("end")


create_services_obj()
