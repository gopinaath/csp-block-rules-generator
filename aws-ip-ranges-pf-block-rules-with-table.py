import requests
import json

# Fetch the JSON data from AWS
response = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
data = response.json()

# Extract the IP ranges
ipv4_ranges = [prefix['ip_prefix'] for prefix in data['prefixes']]
ipv6_ranges = [prefix['ipv6_prefix'] for prefix in data['ipv6_prefixes']]

# Open the output file
with open('aws-block-table.conf', 'w') as f:

    # Begin the pf table for IPv4 ranges
    f.write("table <aws-blocked-ipv4> persist { \n")

    # Loop through the IPv4 ranges and add them to the table
    for ip_range in ipv4_ranges:
        f.write("  " + ip_range + "\n")

    # End the pf table
    f.write("} \n")

    # Begin the pf table for IPv6 ranges
    f.write("table <aws-blocked-ipv6> persist { \n")import requests
import json

# Fetch the JSON data from AWS
response = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
data = response.json()

# Extract the IP ranges
ipv4_ranges = [prefix['ip_prefix'] for prefix in data['prefixes']]
ipv6_ranges = [prefix['ipv6_prefix'] for prefix in data['ipv6_prefixes']]

# Open the output file
with open('aws-block-table.conf', 'w') as f:

    # Begin the pf table for IPv4 ranges
    f.write("table <aws-blocked-ipv4> persist { \n")

    # Loop through the IPv4 ranges and add them to the table
    for ip_range in ipv4_ranges[:-1]:
        f.write("  " + ip_range + ",\n")
    # Write the last IPv4 range without comma
    if ipv4_ranges:
        f.write("  " + ipv4_ranges[-1] + "\n")

    # End the pf table
    f.write("} \n")

    # Begin the pf table for IPv6 ranges
    f.write("table <aws-blocked-ipv6> persist { \n")

    # Loop through the IPv6 ranges and add them to the table
    for ip_range in ipv6_ranges[:-1]:
        f.write("  " + ip_range + ",\n")
    # Write the last IPv6 range without comma
    if ipv6_ranges:
        f.write("  " + ipv6_ranges[-1] + "\n")

    # End the pf table
    f.write("} \n")

    # Write block rules using the tables
    f.write("block in quick on $ext_if from <aws-blocked-ipv4>\n")
    f.write("block in quick on $ext_if from <aws-blocked-ipv6>\n")
    f.write("block out quick on $ext_if to <aws-blocked-ipv4>\n")
    f.write("block out quick on $ext_if to <aws-blocked-ipv6>\n")


    # Loop through the IPv6 ranges and add them to the table
    for ip_range in ipv6_ranges:
        f.write("  " + ip_range + "\n")

    # End the pf table
    f.write("} \n")

    # Write block rules using the tables
    f.write("block in quick on $ext_if from <aws-blocked-ipv4>\n")
    f.write("block in quick on $ext_if from <aws-blocked-ipv6>\n")
    f.write("block out quick on $ext_if to <aws-blocked-ipv4>\n")
    f.write("block out quick on $ext_if to <aws-blocked-ipv6>\n")
