import json
import pandas as pd

# 1. Open and read the JSON file
# Make sure 'data.json' is in the same folder as your script
with open('7_data.json', 'r') as file:
    json_input = json.load(file)

rows = []

# 2. Process the "Types" list
for item in json_input["Types"]:
    # This grabs the top-level key (e.g., "Type")
    type_label = next(iter(item)) 
    data = item[type_label]
    
    # Flatten the structure for Excel
    flattened_row = {
        "Type": type_label,
        "Name": data.get("Name"),
        "Revision": data.get("Revision"),
        "Material": data.get("Material")
    }
    rows.append(flattened_row)

# 3. Create the Excel file
df = pd.DataFrame(rows)
df.to_excel("7_output.xlsx", index=False)

print("Process complete! Check '7_output.xlsx'.")