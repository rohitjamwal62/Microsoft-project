input_data = {"Email":"jacktest123@gmail.com",
              "FirstName":"Ram",
              "LastName":"babu"
              }

import requests,json
# Create Access Token
Refresh_Token = "1000..7ae9dea32fe887e0970d84a08eef22fc"
Client_Id = "1000.3VDWBL8QW74GX3WRB34HWR16E"
Client_Secret = "0d62f85f88a4fa583e1903831cfa25cdf19a2"

url = f"https://accounts.zoho.com/oauth/v2/token?refresh_token={Refresh_Token}&client_id={Client_Id}&client_secret={Client_Secret}&grant_type=refresh_token"
headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
response = requests.request("POST", url, headers=headers)
if response.status_code == 200:
    Token = json.loads(response.text).get('access_token')

# Zoho CRM API endpoint
url = "https://www.zohoapis.com/crm/v2/Leads"
# Zoho CRM API access token
access_token = Token

# Lead details
lead_data = {
    "data": [
        {
            "Last_Name": input_data.get('LastName'),
            "First_Name": input_data.get('FirstName'),
            "Email": input_data.get('Email'),
            "Lead_Status": "Contacted"
        }
    ]
}
# Search criteria to check if lead exists
search_criteria = f"(Email:equals:{input_data.get('Email')})"
# Perform the search request
search_url = f"{url}/search?criteria={search_criteria}"
headers = {
    "Authorization": f"Zoho-oauthtoken {access_token}",
    "Content-Type": "application/json"
}
response = requests.get(search_url, headers=headers)

# Check the response
if response.status_code == 200:
    result = response.json()
    if result.get("info").get("count") > 0:
        # Lead exists, update the lead
        lead_id = result.get("data")[0].get("id")
        update_url = f"{url}/{lead_id}"
        response = requests.put (update_url, headers=headers, data=json.dumps(lead_data))
        if response.status_code == 200:
            print("Lead updated successfully")
        else:
            print("Failed to update lead")
    else:
        # Lead does not exist, create a new lead
        response = requests.post(url, headers=headers, data=json.dumps(lead_data))
        if response.status_code == 201:
            print("Lead created successfully")
        else:
            print("Failed to create lead")
else:
    response = requests.post(url, headers=headers, data=json.dumps(lead_data))
    if response.status_code == 201:
        print("Lead created successfully")
