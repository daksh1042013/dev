import csv
import json

json_output = {"Types": []}
with open('6_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # We extract the 'Type' value to use as a key, 
        # and group the remaining data into a sub-dictionary
        entry = {
            'Type': {
                "Name": row['Name'],
                "Revision": row['Revision'],
                "Material": row['Material']
            }
        }
        json_output["Types"].append(entry)

# 3. Convert to JSON string (or write to file)
final_json = json.dumps(json_output, indent=2)
print(final_json)

# To save to a file:
with open('7_data.json', 'w') as json_file:
    json.dump(json_output, json_file, indent=2)