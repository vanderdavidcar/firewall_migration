# Automation to parsing configurations from Cisco ASA 5500 Series Adaptive Security Appliances to Fortigate (FortiOS)

Challenges that I had to convert all Cisco IOS script from Cisco ASA 5500 Series Adaptive Security Appliances to Fortigate (FortiOS)

Each one were created to specific challenges </br>

## Folder customer

Creating TCP custom services ports
script_02_service.py

Find all address group to create  
script_03_find_grpaddr.py

Create all IP address find ou in source and destination and address-groups
script_04_ipaddr_object.py

Create all incoming rules 
script_05_rules.py

## Folder general_config

Looking for all object-group in Cisco ASA  and convert all IP address to group-address in FortiOS </br>
script_grpaddr.py

Converting all interface to FortiOS
script_collect_intface.py

Converting routing table
script_route_table.py

Looking for peer IPSec active informations
search_ipsec_info.py

fping -a -g 192.168.0.0/24 2>/dev/null > fping.txt

## NMAP
There are many ways to run nmap

Using the simple way</br>
sudo nmap -sT -Sv -O -Pn -v -iL 192.168.0.21

run nmap specifying a file using -iL fping.txt to use only ICMP response.</br>
e.g</br>
sudo nmap -sT -Sv -O -Pn -v -iL fping.txt

## search_nmap.py
Is a function that has a regex patterns to find a specfic information o nmap output file.

## Regex pattern examples
regex = re.compile(r"Nmap scan report for (\w.+)")</br>
regex_os = re.compile(r"Service Info: (\S.+)")
