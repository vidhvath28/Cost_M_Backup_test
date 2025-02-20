import requests
import json
import csv
from azure.identity import ClientSecretCredential

# Azure Credentials (Replace with your values)
TENANT_ID = "014e9593-90f9-4b53-a505-0e1b303fd1d6"
CLIENT_ID = "b4b2a14c-bf6e-4552-8466-b8ed187c1134"
CLIENT_SECRET = "5Ig8Q~B8G6X5oJiV7iX-PmQ0eUmSmSSoEW.z5cux"
SUBSCRIPTION_ID = "22db6142-5c32-4bd4-92c9-445ae5e27415"

# Azure API Endpoint
COST_MANAGEMENT_URL = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"

# Authenticate using ClientSecretCredential
credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
token = credentials.get_token("https://management.azure.com/.default").token

# Request Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Request Body (Fetching Cost Data Grouped by Resource)
payload = {
    "type": "Usage",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {
                "name": "PreTaxCost",
                "function": "Sum"
            }
        },
        "grouping": [
            {"type": "Dimension", "name": "ResourceId"},
            {"type": "Dimension", "name": "ResourceGroup"}
        ]
    }
}

# Make API Request
response = requests.post(COST_MANAGEMENT_URL, headers=headers, json=payload)

# Check Response Status
if response.status_code == 200:
    cost_data = response.json()
    
    # Define CSV File Name
    csv_filename = "azure_cost_data.csv"
    
    # Extract Data and Write to CSV
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Write Header
        writer.writerow(["Resource ID", "Resource Group", "Total Cost (₹)"])
        
        # Write Data Rows
        for row in cost_data.get("properties", {}).get("rows", []):
            writer.writerow(row)
    
    print(f"Azure cost data saved to {csv_filename}")
else:
    print(f"Failed to fetch cost data! Status Code: {response.status_code}")
    print(response.text)
