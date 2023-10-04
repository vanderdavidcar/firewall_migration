## Automation to parsing configurations from Cisco ASA 5500 Series Adaptive Security Appliances to Fortigate (FortiOS)

Challenges that I had to convert all Cisco IOS script from Cisco ASA 5500 Series Adaptive Security Appliances to Fortigate (FortiOS)

Each one were created to specific challenges </br>

### Customer folder

<b>Creating TCP custom services ports</br></b>
script_02_service.py

<b>Find all address group to create</br></b>
script_03_find_grpaddr.py

<b>Create all IP address find ou in source and destination and address-groups</br></b>
script_04_ipaddr_object.py

<b>Create all incoming rules</br></b>
script_05_rules.py

### General_config folder

<b>Looking for all object-group in Cisco ASA  and convert all IP address to group-address in FortiOS </br></b>
script_grpaddr.py

<b>Converting all interface to FortiOS</br></b>
script_collect_intface.py

<b>Converting routing table</br></b>
script_route_table.py

<b>Looking for peer IPSec active informations</br></b>
search_ipsec_info.py

### cvs_manipulation folder

<b>Retrieve files "rules_gp.csv" and "rules.csv" and use jin jatemplate to create all address-object and group-address </br></b>
script_rules.py

