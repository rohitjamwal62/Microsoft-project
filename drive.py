# Genrate Token__________________
import requests,json
Refresh_Token = "1//-L9IrZAbV8u43HaXSdhWjqNDeFA_A9tsvdJuJ37BvfKPNN2NA9DTSH0lmQgFMDW3uwRX7OZU"
Client_Secret = "GOCSPX-"
Client_Id = "782876841430-.apps.googleusercontent.com"

url = "https://oauth2.googleapis.com/token"
payload = f'client_id={Client_Id}&client_secret={Client_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200:
    token = json.loads(response.text).get('access_token')
output = {"token":token}
print(output)



import requests
import json

token = input_data.get('token')
Drive_id = input_data.get('Drive_Id')
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