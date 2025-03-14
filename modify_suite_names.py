import xml.etree.ElementTree as ET

# Parse the combined XML file
tree = ET.parse("test-results.xml")
root = tree.getroot()

# Loop through each testsuite element and modify its name
for testsuite in root.findall("testsuite"):
    old_name = testsuite.get("name")
    # For example, prefix the name with "Modified - "
    new_name = f"Modified - {old_name}"
    testsuite.set("Release Testing", new_name)

# Write the updated XML back to file
tree.write("test-results.xml", encoding="utf-8", xml_declaration=True)
print("Test suite names updated.")
