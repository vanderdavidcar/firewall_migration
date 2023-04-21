#! /usr/bin/env python3

"""
Function Netmiko Connection
"""
from dotenv import load_dotenv
load_dotenv()
import os

username = os.getenv("USERNAME")
passwd = os.getenv("PASSWD")
secret = os.getenv("SECRET")

# Device connection
devices = ["fw-perimeter"]

def netmiko_asa(ip):
    return {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': passwd,
            'secret': passwd
             }
# Netmiko connection
for ipadd in devices:
    iosv = netmiko_asa(str(ipadd))
    print(f"Hostname: {str(ipadd)}\n")