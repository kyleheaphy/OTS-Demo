import glob
import xml.etree.ElementTree as ET

# Create a new root element
root = ET.Element("testsuites")

# Iterate over all XML files in the test results directory
for file in glob.glob("test-results-dir/*.xml"):
    tree = ET.parse(file)
    file_root = tree.getroot()
    # Some files may have <testsuite> as the root while others <testsuites>
    if file_root.tag == "testsuite":
        # Optionally modify the suite name
        old_name = file_root.get("name", "")
        file_root.set("name", f"Modified - {old_name}")
        root.append(file_root)
    elif file_root.tag == "testsuites":
        for testsuite in file_root.findall("testsuite"):
            old_name = testsuite.get("name", "")
            testsuite.set("name", f"Modified - {old_name}")
            root.append(testsuite)

# Write out the merged and modified XML file
tree_out = ET.ElementTree(root)
tree_out.write("test-results.xml", encoding="utf-8", xml_declaration=True)
print("Merged and modified XML file created.")
