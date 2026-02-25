import xml.etree.ElementTree as ET
import pandas as pd

root = ET.parse('6_output.xml')

data_list = []

# 2. Extract data into a list of dictionaries
for type_node in root.findall('Type'):
    row = {'Type': type_node.get('name')}  # Captures 'Part'
    
    for attr in type_node.findall('Attribute'):
        attr_name = attr.get('name')       # e.g., 'Material'
        attr_value = attr.text             # e.g., 'Alloy'
        row[attr_name] = attr_value
        
    data_list.append(row)

# 3. Create DataFrame and export to Excel
df = pd.DataFrame(data_list)
df.to_excel('6_excel_output.xlsx', index=False)

print("Excel file '6_excel_output.xlsx' has been created successfully!")