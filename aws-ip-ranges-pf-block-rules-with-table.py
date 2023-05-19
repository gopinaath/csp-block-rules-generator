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

# Open the output file
with open('aws-block-table.conf', 'w') as f:

    # Begin the pf table
    f.write("table <aws-blocked> persist { \n")

    # Loop through the IP ranges and add them to the table
    for ip_range in ip_ranges:
        f.write("  " + ip_range + "\n")

    # End the pf table
    f.write("} \n")

    # Write block rules using the table
    f.write("block in quick on $ext_if from <aws-blocked>\n")
    f.write("block out quick on $ext_if to <aws-blocked>\n")
