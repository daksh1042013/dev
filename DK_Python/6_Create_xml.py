import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

def csv_to_xml(csv_file_path, xml_file_path):
    # Create the root element <Types>
    root = ET.Element('Types')

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Create <Type name='...'> element
                # We pull the 'Type' column value for the attribute
                type_element = ET.SubElement(root, 'Type', name=row['Type'])
                
                # Iterate through the other columns to create <Attribute> tags
                for header, value in row.items():
                    if header != 'Type':
                        attr = ET.SubElement(type_element, 'Attribute', name=header)
                        attr.text = value

        # Convert to a string and use minidom for pretty-printing (indentation)
        xml_string = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(xml_string)
        pretty_xml = reparsed.toprettyxml(indent="   ")

        # Write to file
        with open(xml_file_path, "w", encoding="utf-8") as f:
            # We skip the default XML declaration to match your requested format
            # by splitting the string after the first newline if necessary
            lines = pretty_xml.split('\n')
            f.write('\n'.join(lines[1:])) 

        print(f"Successfully converted {csv_file_path} to {xml_file_path}")

    except FileNotFoundError:
        print("Error: The CSV file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    # Ensure you have a file named '6_data.csv' in the same directory
    csv_to_xml('6_data.csv', '6_output.xml')