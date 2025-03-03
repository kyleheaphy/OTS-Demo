import os
import xml.etree.ElementTree as ET
import requests
import json
import sys

# Read required environment variables.
qase_api_base_url = os.environ.get("QASE_API_BASE_URL")
qase_api_token = os.environ.get("QASE_API_TOKEN")
qase_project_code = os.environ.get("QASE_PROJECT_CODE")

if not all([qase_api_base_url, qase_api_token, qase_project_code]):
    print("Missing Qase configuration in environment variables. Skipping defect creation.")
    sys.exit(1)

# Parse the test-results.xml file.
try:
    tree = ET.parse("test-results.xml")
    root = tree.getroot()
except Exception as e:
    print(f"Error parsing test results XML: {e}")
    sys.exit(1)

# Extract failed tests from the XML.
failed_tests = []
for testsuite in root.findall("testsuite"):
    for testcase in testsuite.findall("testcase"):
        # Look for a <failure> element.
        failure = testcase.find("failure")
        if failure is not None:
            test_name = testcase.get("name")
            failure_message = failure.text or "No details provided."
            failed_tests.append((test_name, failure_message))

if not failed_tests:
    print("No test failures found. No defects to create.")
    sys.exit(0)

# Create a defect for each failed test.
# (Adjust the endpoint and payload format according to Qase's API documentation.)
for test_name, failure_message in failed_tests:
    payload = {
        "title": f"Test Failure: {test_name}",
        "description": f"Test case '{test_name}' failed with error:\n{failure_message}",
        "status": "Open",  # or other appropriate status
        "project_code": qase_project_code,
    }
    headers = {
        "Content-Type": "application/json",
        "Token": qase_api_token,
    }
    url = f"{qase_api_base_url}/defect"  # Verify this endpoint with Qase API docs.
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code in (200, 201):
        print(f"Defect created for {test_name}.")
    else:
        print(f"Failed to create defect for {test_name}. Response: {response.status_code} {response.text}")
