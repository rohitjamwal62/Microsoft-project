
# Genrate Token__________________
import requests,json
Refresh_Token = "1//-L9IrZAbV8u43HaXSdhWjqNDeFA_A9tsvdJuJ37BvfKPNN2NA9DTSH0lmQgFMDW3uwRX7OZU"
Client_Secret = "-8MSP_8ARhiQe9FvaDT4zX227B16T"
Client_Id = "-pn4vqoq6covt56mf7u0l4p624knrmo7n.apps.googleusercontent.com"

url = "https://oauth2.googleapis.com/token"
payload = f'client_id={Client_Id}&client_secret={Client_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200:
    token = json.loads(response.text).get('access_token')


input_data = {"First_Name":"Jack",
              "Last_Name":"captain",
              "Mail":"jack123@gmail.com"}


import requests,json
Investor_Document_Folder_Id = "126Xe3D1IagkK8DDEvSeEQ92DGuTUlwfR"
token = input_data.get('token')
First_Name = input_data.get('First_Name')
Last_Name = input_data.get('Last_Name')
Name = str(First_Name) +" " + str(Last_Name)
# Create Folder on Drive______________
url = "https://www.googleapis.com/drive/v3/files"
payload = json.dumps({
  "name": Name,
  "mimeType": "application/vnd.google-apps.folder",
  "parents": [Investor_Document_Folder_Id]
})
headers = {
  'Authorization': f'Bearer {token}',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200:
    Drive_id =  json.loads(response.text).get('id')
output = {"Drive_Id":Drive_id}

# Share folder_________________
url = f"https://www.googleapis.com/drive/v3/files/{Drive_id}/permissions"
payload = json.dumps({
  "role": "writer",
  "type": "user",
  "emailAddress": input_data.get('Mail')
})
headers = {
  'Authorization': f'Bearer {token}',
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
output = {"response":response.text}
print(output,"================")