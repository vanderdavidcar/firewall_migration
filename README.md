## Automation to parsing configurations from Cisco ASA 5500 Series Adaptive Security Appliances to Fortigate (FortiOS)

Challenges that I had to convert all Cisco IOS script from Cisco ASA 5500 Series Adaptive Security Appliances to Fortigate (FortiOS)

Each one were created to specific challenges </br>

### Customer folder

Creating TCP custom services ports</br></b>
script_02_service.py

Find all address group to create</br>
script_03_find_grpaddr.py

Create all IP address find ou in source and destination and address-groups</br>
script_04_ipaddr_object.py

Create all incoming rules</br>
script_05_rules.py

### General_config folder

Looking for all object-group in Cisco ASA  and convert all IP address to group-address in FortiOS </br>
script_grpaddr.py

Converting all interface to FortiOS</br>
script_collect_intface.py

Converting routing table</br>
script_route_table.py

Looking for peer IPSec active informations</br>
search_ipsec_info.py