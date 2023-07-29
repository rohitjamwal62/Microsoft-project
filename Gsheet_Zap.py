input_data = {
            "Group":"Fruition Prospects",
            "Lead Status":"3. NEW",
            "First Name":'Bess & Boyd Investment Holdings, LLC',
            "Last Name":"Clay and Bess Edwards",
            "Initial Interest":"Y",
            "SC Date":"2023-07-07T22:12:50.456Z",
            "SC Amount":"",
            "Tagged in MC":"Y"
        }

# Zap1__________________________________________________________________
import requests,json
from datetime import datetime
current_date = datetime.now().strftime("%m/%d/%y")

# Create Access Token
Refresh_Token = "1//04_--L9IrSwzzYDP61zjXv72XxWhCpDFgAG_jn2uoxqOsMU5OQuzLvtUZ3AUgO-pW2mXpdVeVrxk"
Client_Id = "311584547418-.apps.googleusercontent.com"
Cleint_Secret = "GOCSPX-"

url = f"https://accounts.google.com/o/oauth2/token?client_id={Client_Id}&client_secret={Cleint_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token"
headers = {'Accept': 'application/json'}
response = requests.request("POST", url, headers=headers)
if response.status_code == 200:
    Token = json.loads(response.text).get('access_token')



# Zap2_______________________________________________________________________
import requests,json
# Zap2
Group = input_data.get('Group')
Lead_Status = input_data.get('Lead Status')
First_Name = input_data.get('First Name')
Last_Name = input_data.get('Last Name')
Initial = input_data.get('Initial Interest')
SC_Date_Format = input_data.get('SC Date')
SC_Amount = input_data.get('SC Amount')
Tagged_in_MC = input_data.get('Tagged in MC')
Package_Sent = current_date
# Token = input_data.get('Token')
SC_Date = str(SC_Date_Format).split('T')[0]


if First_Name == None:
    First_Name = ''
Google_Form_Name = str(First_Name)+" "+str(Last_Name)
output = {"output":Google_Form_Name}

Sheet_Id = "1dNXsYtPlOft3Z0oioUbdIIIhrciHhis8wf91iEs"
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
                if Google_Form_Name == Name:
                    Create_Range = f"A{count}:O{count}"
                    print("Updating records.........",Create_Range)
                    # Update sheet
                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{Sheet_Id}/values/{Create_Range}?valueInputOption=USER_ENTERED"
                    Records = [Group,Lead_Status,First_Name,Last_Name,'','','','','',Initial,'',SC_Date,SC_Amount,Tagged_in_MC,Package_Sent]
                    print(Records,"___________")
                    payload = json.dumps({"values": [Records]})
                    response = requests.request("PUT", url, headers=GoogleSheet_Headers, data=payload)
                    if response.status_code == 200:
                        output = {"Response":response.text}
                        print(output,"Update")
            count +=1
    except:
        pass

    if Google_Form_Name not in Google_Sheet_Records:
        # create row
        print("Creating records...................")
        Records = [Group,Lead_Status,First_Name,Last_Name,'','','','','',Initial,'',SC_Date,SC_Amount,Tagged_in_MC,Package_Sent]
        Range = "A355:O355"
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{Sheet_Id}/values/{Range}:append?valueInputOption=USER_ENTERED"
        payload = json.dumps({"values": [Records]})
        response = requests.request("POST", url, headers=GoogleSheet_Headers, data=payload)
        if response.status_code == 200:
            sheet = json.loads(response.text)
            output = {"Response":sheet}
            print(output,"Create") 