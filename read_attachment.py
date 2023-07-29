import requests,json,base64,PyPDF2,re,time,os
from datetime import datetime
from fuzzywuzzy import fuzz

Client_Id = "f7fdd1a3-eb30363bb81ef052"
Client_Secret = "QA0FHktwZuvoIucJP8jJJ6tulpQjrNb2w"
Tenant_Id = "bf0022b-8e19-f444e9fa7ced"
Refresh_Token = "0.AUYAuyfRE6fp87aPR_fcw685PoJ02O7ge8FKAAEw.AgABAAEAAAAtyolDObpQQ5VtlI4uGjEPAgDs_wUA9P9JD58qNcid3A2pAn1nyorUC8JJxpPLvfdH1PpSqZNq1jKHxzPmxyhRiCnBs7IYC6L4-C9a5nQ00mRcdGOd0Agn5B2dS8xq2VMxqOWDPBUo_Yij_a6XMgYK24emCBYGgrYNmIqwWhD56SrqrmQhKrRS1tP6d6b84Q6OApF4VAGDOBD5bx3y9aQH_AoXtbEO91sMOFnoi_nrjHuU9R-uJg4FX47ya2CaMVxehR1RuTHbisa1cu9X15C9AN-3X59S_Rgq5Xqb4Guq92svhoe-fBqFuWCWb88384zr47r-YDr4YQJR3-14_ZnWO_wxMT4rM_o5Fz4hgYEYP259lbI-JFOvlIhbo0UDc5w0iyIeOINq5bGB2w4t6i1mDW9EHDGCJap2w-1ev96jPt6a1rJHHOhGZSRf3GM6m_rMlwySBKB91wqHsvpZQWEJdR9OoybPozxjXVH5F8oQxIdFcnOnYEbLjetaDFmPiwJmyfDbK6qImbVCYmR6foewqOB8U9Zh33VGfCC2NBctLp9Y6nDWi3seEVTFDhg8tJn6gk7FvdxGPKYQ_KRSH9SqtXR90QGRIx1IpRZOa5-7ytqYl-Ak-9jWGf55drn0x8oLG78c6u23OXtR00RL4-Hb60hfunNoHS1oQcxFNHnU4ZERe2pIHRBGj9CdaC6pH5WDg4VbFTcCXWgVjYruktzz-l3mGqxPnozkrFnYgtDeiUzHulCCb42pTTBdougtbfXfNKLfMQ3osgwa41gwdymeUJbnfCs05E5-RQIyeGLNG15Fm6UGKKgQubycbl471F1qLtJjOQW9-Fjn6wsj-ruq7cykTloiHftCpoHV"

# AgencyEmail = "transfer.agency@navconsulting.net"
AgencyEmail = "mapplecode2020@gmail.com"
AgencySubject = "New Investor Subscription Package for Fruition Capital Fund I (Ref: 1450781)"
EmailFile_Name = "tempates.txt"
SearchEmail = list()


def find_closest_match(match_str, names_list):
    best_match_ratio = -1
    closest_matches = []
    for name in names_list:
        ratio = fuzz.token_sort_ratio(match_str, name)
        if ratio > best_match_ratio:
            best_match_ratio = ratio
            closest_matches = [name]
        elif ratio == best_match_ratio:
            closest_matches.append(name)
    return closest_matches

def create_active_audience_member(prospective_member):
    url = "https://us17.api.mailchimp.com/3.0/lists/c2e8bc9ba"
    # Extract merge fields from prospective_member
    address = prospective_member.get('merge_fields', {}).get('ADDRESS', "")
    phone = prospective_member.get('merge_fields', {}).get('PHONE', "")
    Lname = prospective_member.get('merge_fields', {}).get('LNAME', "")
    Fname = prospective_member.get('merge_fields', {}).get('FNAME', "")
    
    # Extract stats and locations if available, otherwise set them to an empty dictionary
    stats = prospective_member.get('stats', {}) if prospective_member.get('stats') else {}
    locations = prospective_member.get('location', {}) if prospective_member.get('location') else {}
    
    # Create the payload for the API request
    payload = {
        "members": [
            {
                "id": prospective_member.get('id', ""),
                "email_address": prospective_member.get('email_address', ""),
                "status": prospective_member.get('status', ""),
                "full_name": prospective_member.get('full_name', ""),
                "unique_email_id": prospective_member.get('unique_email_id', ""),
                "contact_id": prospective_member.get('contact_id', ""),
                "web_id": prospective_member.get('web_id', ""),
                "email_type": prospective_member.get('email_type', ""),
                "consents_to_one_to_one_messaging": True,
                
                "merge_fields": {
                    "FNAME": Fname,
                    "LNAME": Lname,
                    "ADDRESS": address,
                    "PHONE": phone,
                },
                "stats": stats,
                "ip_signup": prospective_member.get('ip_signup', ""),
                "timestamp_signup": prospective_member.get('timestamp_signup', ""),
                "ip_opt": prospective_member.get('ip_opt', ""),
                "timestamp_opt": prospective_member.get('timestamp_opt', ""),
                "member_rating": prospective_member.get('member_rating', ""),
                "last_changed": prospective_member.get('last_changed', ""),
                "language": prospective_member.get('language', ""),
                "vip": False,
                "email_client": prospective_member.get('email_client', ""),
                "location": locations,
                
                "source": prospective_member.get('source', ""),
                "tags": ["AEFI Investors"],
                "sync_tags": False,
                "update_existing": False
            }
        ]
    }

    headers = {'Authorization': 'Basic YW55c3RyaW5nOjE1OThkNmQ2OGUxM2ViNDUzZDlkOGMxMTc2NzZiMTViLXVzMTc=','Content-Type': 'application/json',}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    created_records = json.loads(response.text)
    return created_records

pdf_File_Name = "WireEmail.pdf"
def save_base64_to_pdf(base64_data):
    byte_data = base64.b64decode(base64_data)
    with open(pdf_File_Name, 'wb') as pdf_file:
        pdf_file.write(byte_data)


def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        pdf_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()
    return pdf_text

# Create Token
def Getnerate_Token():
    url = f"https://login.microsoftonline.com/{Tenant_Id}/oauth2/v2.0/token"
    payload = f'client_id={Client_Id}&scope=User.Read%20Mail.Read&refresh_token={Refresh_Token}&grant_type=refresh_token&client_secret={Client_Secret}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        Token = json.loads(response.text).get('access_token')
        return Token
   
Token = Getnerate_Token()

Outlook_Token = Token
def SendMail(MailFirstName,Email,FileName):
    with open(FileName,'r') as file:
        data = file.read()
        Subject = (data.split('\n')[0])
        Email_Body_Content = data.replace(Subject,'').replace('FIRSTNAME',f'{MailFirstName}')

        # Send Email_____
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        payload = {
            "message": {
                "subject": Subject,
                "body": {
                    "contentType": "Text",
                    "content": Email_Body_Content
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": Email
                        }
                    }
                ]
            },
            "saveToSentItems": "true"
        }
        headers = {'Authorization': f'Bearer {Outlook_Token}','Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.text


SaveName = list()
# Read Inbox message
ReadInbox_Url = "https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages"
headers = {'Authorization': f'Bearer {Token}','Content-Type': 'application/json'}
response = requests.request("GET", ReadInbox_Url, headers=headers)
if response.status_code == 200:
    Records = json.loads(response.text).get('value')[0]
    Store_Id = Records.get('id')
    Subject = Records.get('subject')
    CreatedDateTime = Records.get('createdDateTime')
    Sender_Email = Records.get('sender').get('emailAddress').get('address')
    # if str(Subject).lower() == "wire detail report" and Sender_Email == "transfer.agency@navconsulting.net":
    # if str(Subject).lower() == "wire detail report":
    if str(Subject).lower() == "neha test wire detail report":
        print("Wire Email is reveived__________________________")
      
        # Read attachment
        url = f"https://graph.microsoft.com/v1.0/me/messages/{Store_Id}/attachments"
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            Attachment_Values = json.loads(response.text).get('value')
            for attachments in Attachment_Values:
                Store_Attachment = attachments.get('contentBytes')
                save_base64_to_pdf(Store_Attachment) # Convert bytes to pdf
                time.sleep(20)
                pdf_text = read_pdf(pdf_File_Name) #Read Pdf files
                NameFrom_Pdf = str(pdf_text).split('Originator')[1].split('\n')[1].split('-')[1].split(',')[0]
                # print(NameFrom_Pdf,"-----")

                Additional_Information = str(pdf_text).split('Additional Information')[1].split('\n')[1].split('FBO')[1]
                print(Additional_Information,"-----")

                # Update Googlesheet________________________________________________________
                current_date = datetime.now()
                Fund_Received = current_date.strftime("%m/%d/%y")
                # Create Access Token
                Refresh_Token = "1//04_-pBBkr5f__CgYIARAAGAQSNwF-L9IrSwzzYDP61zjXv72XxWhCpDFgAG_jn2uoxqOsMU5OQuzLvtUZ3AUgO-pW2mXpdVeVrxk"
                Client_Id = "311584547418-9vdjoclj4a7thqb0oovdbbg46ucpdh13.apps.googleusercontent.com"
                Cleint_Secret = "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"
                url = f"https://accounts.google.com/o/oauth2/token?client_id={Client_Id}&client_secret={Cleint_Secret}&refresh_token={Refresh_Token}&grant_type=refresh_token"
                headers = {'Accept': 'application/json'}
                response = requests.request("POST", url, headers=headers)
                if response.status_code == 200:
                    Token = json.loads(response.text).get('access_token')
                Sheet_Id = "1dNXsYtPlOft3Z0GclLoioUbdIIIhrciHhis8wf91iEs"
                GoogleSheet_Headers = {'Authorization': f'Bearer {Token}','Content-Type': 'application/json'}
                # Get All Sheet Records
                url = f"https://sheets.googleapis.com/v4/spreadsheets/{Sheet_Id}/values/A1:Z"
                response = requests.request("GET", url, headers=GoogleSheet_Headers)
                count = 1
                
                if response.status_code == 200:
                    Records = json.loads(response.text).get('values')
                    Google_Sheet_Records = [(rec[2]+" "+ rec[3]) for rec in Records if len(rec) > 1 and len(rec)>3]  
                    Store_Matched_Name = list()    
                    try: 
                        Name_list = list()
                        for rec in Records:
                            if len(rec) > 1 and len(rec) > 3:
                                Name = rec[2] + " " + rec[3]
                                Name_list.append(Name)
                        # match string with pdf file
                        match_str = [Additional_Information]
                        for matchstr in match_str:
                            closest_matches = find_closest_match(matchstr, Name_list)
                        for match in closest_matches:
                            Store_Matched_Name.append(match)
                        # End match string
                        MatchedName = Store_Matched_Name[0]
                        for rec in Records:
                            if len(rec) > 1 and len(rec) > 3:
                                Name = rec[2] + " " + rec[3]
                                if MatchedName == Name:
                                    # print(Name,"======================================")
                                    SaveName.append(Name)       
                                    # SaveName.append({"FirstName":FirstName,"LastName":LastName})
                                    Create_Range = f"S{count}"
                                    print("Updating records.........",Create_Range)
                                    # Update sheet
                                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{Sheet_Id}/values/{Create_Range}?valueInputOption=USER_ENTERED"
                                    Records = Fund_Received
                                    Records = ["6/29/23"]
                                    payload = json.dumps({"values": [Records]})
                                    response = requests.request("PUT", url, headers=GoogleSheet_Headers, data=payload)
                                    if response.status_code == 200:
                                        output = {"Response":response.text}
                                        
                            count +=1
                    except:
                        pass
                ZohoNames = str(SaveName[0]).split(' ')
                ZohoF = ZohoNames[0]
                ZohoL = ZohoNames[1]
                ZohoName = str(ZohoF) +" " + str(ZohoL)
                
                Individual = ZohoName
                MailFirstName = ZohoF
                
                # Zoho CRM______________________________________________________________________________
                # Create Access Token
                Refresh_Token = "1000.a64708f7c93c282923109c84b11f14c7.7ae9dea32fe887e0970d84a08eef22fc"
                Client_Id = "1000.3VDWBL8QW74GXJWD0M3WRB34HWR16E"
                Client_Secret = "0d62f85f88a4fa583e712331903831cfa25cdf19a2"

                url = f"https://accounts.zoho.com/oauth/v2/token?refresh_token={Refresh_Token}&client_id={Client_Id}&client_secret={Client_Secret}&grant_type=refresh_token"
                headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
                response = requests.request("POST", url, headers=headers)
                if response.status_code == 200:
                    access_token = json.loads(response.text).get('access_token')
                # Search Lead
                url = f"https://www.zohoapis.com/crm/v4/Leads/search?criteria=(Full_Name:equals:{ZohoName})"
              
                Zoho_headers = {
                     "Authorization": f"Zoho-oauthtoken {access_token}",
                    'Content-Type': 'application/json'
                    }
                response = requests.request("GET", url, headers=Zoho_headers)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("info").get("count") > 0:
                        # Lead exists, update the lead
                        lead_id = result.get("data")[0].get("id")
                        Lead_Email = result.get("data")[0].get("Email")
                        SearchEmail.append(Lead_Email)
                        update_url = f"https://www.zohoapis.com/crm/v2/Leads/{lead_id}"
                        payload = json.dumps({
                        "data": [
                            {
                            "Lead_Status": "Investors",
                            "Company": "Pre-Qualified"
                            }
                        ]
                        })
                        response = requests.request("PUT", update_url, headers=Zoho_headers, data=payload)
                        if response.status_code == 200:
                            print("Successfully Update Records into the Zoho CRM")
                # MailChimp_____________________________________________
                # Get Prospective Investor Audience
                Prospective_Investore_Id = "e564b58ee3"
                Audience_Url = "https://us17.api.mailchimp.com/3.0/lists/"
                url = f"{Audience_Url}{Prospective_Investore_Id}/members?count=10000"
                headers = {'Authorization': 'Basic YW55c3RyaW5nOjE1OThkNmQ2OGUxM2ViNDUzZDlkOGMxMTc2NzZiMTViLXVzMTc=','Content-Type': 'application/json',}
                response = requests.request("GET", url, headers=headers)
                if response.status_code == 200:
                    Prospective_Records = json.loads(response.text).get('members')
                    for Procpective_member in Prospective_Records:
                        Prospective_Full_Name = Procpective_member.get('full_name')
                        Prospective_Email_Address =  Procpective_member.get('email_address')
                        if (Individual).lower() == str(Prospective_Full_Name).lower():
                            # Copy Propective Audience to Active Audience__________________
                            data = create_active_audience_member(Procpective_member)
                            print("Copy the data into Active Audience Successfully")
                # Send Email_____________________
                AgencyEmail = "transfer.agency@navconsulting.net"
                AgencyEmail = "mapplecode2020@gmail.com"
                EmailFile_Name = "transferAgency.txt"
                SendMail(MailFirstName,AgencyEmail,EmailFile_Name) #Send an email from me to transfer.agency@navconsulting.net
                time.sleep(1)

                Confirmaion_Mail = SearchEmail[0]
                Confirmaion_Mail = "mapplecode2020@gmail.com"
                EmailFile_Name = "ConfirmationMail.txt"
                SendMail(MailFirstName,AgencyEmail,EmailFile_Name) # Send the Confirmation of Your Wire Email
                time.sleep(60) 

                try:
                    os.remove(pdf_File_Name)
                    print(f"File {pdf_File_Name} removed successfully.")
                except FileNotFoundError:
                    print(f"File {pdf_File_Name} not found.")
                except PermissionError:
                    print(f"Permission denied to delete {pdf_File_Name}. Make sure you have the necessary permissions.")
                except Exception as e:
                    print(f"Error occurred while deleting {pdf_File_Name}: {e}")
   
