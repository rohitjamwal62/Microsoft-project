input_data = {"Name":"Robert Jackson ,Jason Ehrlich"}


import requests,json

DocuSign_Names = input_data.get('Name')
Doc_Names = str(DocuSign_Names).strip().split(',')

Refresh_Token = "1//04_-pBBkr5f__CGAQSNwF-L9IrSwzzYDP61zjXv72XxWhCpDFgAG_jn2uoxqOsMU5OQuzLvtUZ3AUgO-pW2mXpdVeVrxk"
Client_Id = "311584547418-9vdjoclj4b0oovdbbg46ucpdh13.apps.googleusercontent.com"
Cleint_Secret = "GOCSPX-jgvel7EFWT4qzqbYIQLS5K"
Sheet_Id = "1dNXsYtPlOft3Z0GclLoioUbdiHhis8wf91iEs"

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
    Google_Sheet_Records = [(rec[2]+" "+ rec[3]) for rec in Records if len(rec) > 1]
    try:
      for rec in Records:
          if len(rec) >1:
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