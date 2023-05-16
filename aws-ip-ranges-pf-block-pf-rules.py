import requests
import json

# Fetch the JSON data from AWS
response = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
data = response.json()

# Extract the IP ranges
ipv4_ranges = [prefix['ip_prefix'] for prefix in data['prefixes']]
ipv6_ranges = [prefix['ipv6_prefix'] for prefix in data['ipv6_prefixes']]

# Combine both ipv4 and ipv6 ranges
ip_ranges = ipv4_ranges + ipv6_ranges

# Open the output file for OpenBSD firewall (PF)
with open('aws-block.conf', 'w') as f:

    # Begin the pf ruleset for inbound traffic
    f.write("# Inbound rules\n")
    f.write("block in quick on $ext_if from {\n")

    # Loop through the IP ranges and add them to the ruleset
    for ip_range in ip_ranges:
        f.write("  " + ip_range + "\n")

    # End the pf ruleset
    f.write("}\n\n")

    # Begin the pf ruleset for outbound traffic
    f.write("# Outbound rules\n")
    f.write("block out quick on $ext_if to {\n")

    # Loop through the IP ranges and add them to the ruleset
    for ip_range in ip_ranges:
        f.write("  " + ip_range + "\n")

    # End the pf ruleset
    f.write("}\n")


# Open the output file for Linux firewall (UFW)
with open('aws-block-ufw.conf', 'w') as f:

    # Loop through the IP ranges and generate UFW rules for incoming traffic
    for ip_range in ip_ranges:
        f.write(f"sudo ufw deny in from {ip_range}\n")

    # Loop through the IP ranges and generate UFW rules for outgoing traffic
    for ip_range in ip_ranges:
        f.write(f"sudo ufw deny out to {ip_range}\n")