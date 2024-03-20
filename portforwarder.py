import json


def delete_entry(mac_address):
    with open('user_data.json', 'r') as file:
        data = json.load(file)

    removed_entry = None
    updated_data = []
    for entry in data:
        if entry['macaddress'] != mac_address:
            updated_data.append(entry)
        else:
            removed_entry = entry

    if removed_entry:
        print(f"Entry removed: {removed_entry}")

    with open('user_data.json', 'w') as file:
        json.dump(updated_data, file, indent=4)

# Example usage: delete entry with MAC address '24:b1:05:72:7c:4e'
delete_entry('24:b1:05:72:7c:4e')
