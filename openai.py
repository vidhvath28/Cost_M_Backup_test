from azure.identity import ClientSecretCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from datetime import datetime, timedelta
from dateutil import parser  
import csv

# Replace with your Azure credentials
TENANT_ID = "014e9593-90f9-4b53-a505-0e1b303fd1d6"
CLIENT_ID = "b4b2a14c-bf6e-4552-8466-b8ed187c1134"
CLIENT_SECRET = "5Ig8Q~B8G6X5oJiV7iX-PmQ0eUmSmSSoEW.z5cux"
SUBSCRIPTION_ID = "22db6142-5c32-4bd4-92c9-445ae5e27415"



# Authenticate
credential = ClientSecretCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
client = ConsumptionManagementClient(credential, SUBSCRIPTION_ID)

# Define the scope (subscription-level)
scope = f"/subscriptions/{SUBSCRIPTION_ID}"

# Fetch usage details
usage_details = client.usage_details.list(scope=scope)

# Debug: Print all service names to check if "Text to Speech" is included
print("🔍 Checking available services...\n")
all_services = set()  # Store unique service names
for item in usage_details:
    all_services.add(item.product)  # Collect all product names

# Print found services
for service in sorted(all_services):
    print(f"Service Found: {service}")

# Exit script after showing available services
exit()
