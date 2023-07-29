input_data = {"Name":"Bess & Boyd Investment Holdings, LLC,Jacktest"}

import requests,json

Investor_Document_Folder_Id = "12D1IagkK8DDEvSeEQ92DGuTUlwfR"
Name = input_data.get('Name')
if ',' in Name:
    name = str(Name).split(',')[0]
else:
    name = Name

Refresh_Token = "1//-RWCgYIARAAGAQSNwF-L9Irqc5u8owLHhfbuX9eUNAsyUm6VcvEsYSZnCokW4bnPvjFjfpxhpD8HXxlvjMxtfOuewY"
Client_Id = "-pn4vqoq6covt56mf7u0l4p624knrmo7n.apps.googleusercontent.com"
Cleint_Secret = "GOCSPX-"

# Create Access Token
url = f"https://accounts.google.com/o/oauth2/token?client_id={Client_Id}&client_secret={Cleint_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token"
headers = {'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers)
if response.status_code == 200:
    Token = json.loads(response.text).get('access_token')



# Create Folder on Drive______________
url = "https://www.googleapis.com/drive/v3/files"
payload = json.dumps({
  "name": name,
  "mimeType": "application/vnd.google-apps.folder",
  "parents": [Investor_Document_Folder_Id]
})
headers = {'Authorization': f'Bearer {Token}','Content-Type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    Drive_id =  json.loads(response.text).get('id')
    Name = json.loads(response.text).get('name')
output = {"Drive_Id":Drive_id,"Name":name}



# UPdate sheet_________________________________________
input_data = {"Name":"jack"}
import requests,json
DocuSign_Names = input_data.get('Name')
Doc_Names = str(DocuSign_Names).strip().split(',')

Refresh_Token = "1//04_-pBBkr5f__CgYIARAAGAQSNwF-L9IrSwzzYDP61zjXv72XxWhCpDFgAG_jn2uoxqOsMU5OQuzLvtUZ3AUgO-pW2mXpdVeVrxk"
Client_Id = "311584547418-9vdjoclj4a7thqb0oovdbbg46ucpdh13.apps.googleusercontent.com"
Cleint_Secret = "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"
Sheet_Id = "1dNXsYtPlOft3Z0GclLoioUbdIIIhrciHhis8wf91iEs"

# Create Access Token
url = f"https://accounts.google.com/o/oauth2/token?client_id={Client_Id}&client_secret={Cleint_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token"
headers = {'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers)
if response.status_code == 200:
    Token = json.loads(response.text).get('access_token')

GoogleSheet_Headers = {'Authorization': f'Bearer {Token}','Content-Type': 'application/json'}
# Get All Sheet Records
url = f"https://sheets.googleapis.com/v4/spreadsheets/{Sheet_Id}/values/A1:Z"
response = requests.request("GET", url, headers=GoogleSheet_Headers)
count = 1
if response.status_code == 200:
    Records = json.loads(response.text).get('values')
    Google_Sheet_Records = [(rec[2]+" "+ rec[3]) for rec in Records if len(rec) > 1 and len(rec)>3]
    try:
      for rec in Records:
          if len(rec) > 1 and len(rec)>3:
              Name = rec[2]+" "+rec[3]        
              if Name in Doc_Names:
                  Create_Range = f"P{count}"
                  print("Updating records.........",Create_Range)
                  # Update sheet
                  url = f"https://sheets.googleapis.com/v4/spreadsheets/{Sheet_Id}/values/{Create_Range}?valueInputOption=USER_ENTERED"
                  Records = ['Y']
                  payload = json.dumps({"values": [Records]})
                  response = requests.request("PUT", url, headers=GoogleSheet_Headers, data=payload)
                  if response.status_code == 200:
                      output = {"Response":response.text}
                      print(output,"Update")
          count +=1
    except:
        pass


# Matching Drive Folder Name___________
input_data = {"Name":"Bess & Boyd Investment Holdings, LLC,Jacktest"}


Name = input_data.get('Name')
if ',' in Name:
    name = str(Name).split(',')[0].strip()
else:
    name = Name.strip()

import requests,json
Refresh_Token = "1//049QP_6omxfJ9CgYIARAAGAQSNwF-L9IrZAbV8u43HaXSdhWjqNDeFA_A9tsvdJuJ37BvfKPNN2NA9DTSH0lmQgFMDW3uwRX7OZU"
Client_Secret = "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"
Client_Id = "782876841430-pn4vqoq6covt56mf7u0l4p624knrmo7n.apps.googleusercontent.com"
# Genrate Token__________________
url = "https://oauth2.googleapis.com/token"
payload = f'client_id={Client_Id}&client_secret={Client_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200:
    token = json.loads(response.text).get('access_token')

Investor_Document_Folder_Id = "126Xe3D1IagkK8DDEvSeEQ92DGuTUlwfR"
url = f"https://www.googleapis.com/drive/v3/files?q='{Investor_Document_Folder_Id}'+in+parents&fields=files(id, name)"
headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
response = requests.request("GET", url, headers=headers)

if response.status_code ==200:
    Collect_Folders_Names = json.loads(response.text).get('files')
    for folder in Collect_Folders_Names:
        FolderName = str(folder.get('name')).strip()
        FolderId = folder.get('id')
        if name == FolderName:
            output = {"Folder Name":FolderName,"FolderId":FolderId}
            print(output)