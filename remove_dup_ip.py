#! /usr/bin/env python3

# Object names
objects = ["fontnet", "redes"]

# Using external data to remove duplicated IP addresses
for fi in objects:
    if fi in objects:
        with open(f'{fi}', 'r') as fp:
            address = fp.read().split()
            i = '\n'.join(address)

        new_ips = []

        final_newlist = list(dict.fromkeys(address))
        new_list = '\n'.join(final_newlist)
        print(f'Print new list: {fi}_paci\n\n{new_list}')

        with open(f'{fi}_new_ips.txt', 'w') as f:
            f.write(f'{new_list}')    