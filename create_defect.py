import os
import xml.etree.ElementTree as ET
import requests
import json
import sys
import base64

# Read required environment variables.
qase_api_base_url = os.environ.get("QASE_API_BASE_URL")
qase_api_token = os.environ.get("QASE_API_TOKEN")
qase_project_code = os.environ.get("QASE_PROJECT_CODE")

# Jira configuration
jira_domain = os.environ.get("JIRA_DOMAIN")  # e.g., "optimus-us"
jira_email = os.environ.get("JIRA_EMAIL")
jira_api_token = os.environ.get("JIRA_API_TOKEN")
jira_project_key = os.environ.get("JIRA_PROJECT_KEY")  # e.g., "QTR"

# Check required Qase configuration.
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

def create_qase_defect(test_name, failure_message):
    """Create a defect in Qase and return its ID if successful."""
    payload = {
        "title": f"Test Failure: {test_name}",
        "actual_result": f"Test case '{test_name}' failed with error:\n{failure_message}",
        "severity": 2,  # adjust severity as needed
        "status": "Open",
        "code": qase_project_code,
    }
    headers = {
        "Content-Type": "application/json",
        "Token": qase_api_token,
    }
    url = f"{qase_api_base_url}/defect"
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code in (200, 201):
        print(f"Defect created for {test_name}.")
        # Assuming the response JSON contains the defect ID in result.id
        try:
            result = response.json().get("result", {})
            defect_id = result.get("id")
            return defect_id
        except Exception as e:
            print("Error parsing defect creation response:", e)
            return None
    else:
        print(f"Failed to create defect for {test_name}. Response: {response.status_code} {response.text}")
        return None

def create_jira_issue(test_name, failure_message):
    """Create a Jira issue for the failed test and return the Jira issue key if successful."""
    # Prepare the Basic Auth header using Python.
    auth_str = f"{jira_email}:{jira_api_token}"
    encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    jira_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_auth}"
    }
    # Jira API endpoint to create an issue.
    url = f"https://{jira_domain}.atlassian.net/rest/api/3/issue"
    # Define the JSON payload using an f-string for interpolation.
    jira_payload = {
        "fields": {
            "project": {"key": jira_project_key},
            "summary": f"Test Failure: {test_name}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Test case '{test_name}' failed with error:\n{failure_message}"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Bug"}
        }
    }
    response = requests.post(url, data=json.dumps(jira_payload), headers=jira_headers)
    if response.status_code in (200, 201):
        try:
            jira_issue = response.json()
            jira_issue_key = jira_issue.get("key")
            print(f"Jira issue {jira_issue_key} created for {test_name}.")
            return jira_issue_key
        except Exception as e:
            print("Error parsing Jira creation response:", e)
            return None
    else:
        print(f"Failed to create Jira issue for {test_name}. Response: {response.status_code} {response.text}")
        return None

def update_qase_defect_with_jira_link(defect_id, jira_issue_key):
    """Update a Qase defect with a link to the corresponding Jira issue."""
    payload = {
        "jira_link": f"https://{jira_domain}.atlassian.net/browse/{jira_issue_key}"
    }
    headers = {
        "Content-Type": "application/json",
        "Token": qase_api_token,
    }
    url = f"{qase_api_base_url}/defect/{defect_id}"
    response = requests.put(url, data=json.dumps(payload), headers=headers)
    if response.status_code in (200, 201):
        print(f"Qase defect {defect_id} updated with Jira link.")
    else:
        print(f"Failed to update Qase defect {defect_id}. Response: {response.status_code} {response.text}")

# Process each failed test.
for test_name, failure_message in failed_tests:
    defect_id = create_qase_defect(test_name, failure_message)
    if defect_id:
        jira_issue_key = create_jira_issue(test_name, failure_message)
        if jira_issue_key:
            update_qase_defect_with_jira_link(defect_id, jira_issue_key)
