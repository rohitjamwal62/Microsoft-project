Automation Details
•	Trigger 1: When a soft commitment form is submitted on the Google Form:
o	Create a folder in the fund's Google Drive account (subfolder: Fund Admin -> Investor Documents) with the naming convention "FIRSTNAME LASTNAME" and share it with the submitter via the email address they provided (add them to the folder and have Google Drive send the link)
•	Note: the goal is to add them to the folder such that only they have access to it (and not anyone with the link)
o	Add the form submitter to MailChimp if they're not already there, or update their profile if they are already there and:
•	Set the submitter's Audience to "Prospective Investors" and apply Tags for "Fruition Prospects" and "AEFI Subscribers"
o	Send the Next Steps Email (see the contents at the bottom of this document)
•	Note: since I only have the free version of MailChimp this will need to be done through an Outlook Zap rather than an Automation in Mailchimp
•	Ideally the Next Steps Email would include their custom link to the Google Drive folder that was created for them, but if this is not possible or is too much work then having Google send them the access link directly when the folder is set up is sufficient
o	Send the Subscription Package (see the only item in Templates) to the submitter via DocuSign
o	Add the submitter as a Lead in Zoho CRM or update their profile if they're already there; fields to include are below
•	Company: leave as-is if updating a record, if a new record set to "Fruition Prospects"
•	First Name: from Google Form
•	Last Name: from Google Form
•	Email: from Google Form
•	Lead Status: Contacted
o	Add the submitter as a row in the Google Sheets Equity Tracker or update their row if they’re already there; if they are already there then only update those columns which don't already have values in them; values to include are below:
•	Group: Fruition Prospects
•	Lead Status: 3. NEW
•	First Name: from Google Form
•	Last Name: from Google Form
•	Initial Interest: Y
•	SC Date: date Google Form was submitted
•	SC Amount: amount indicated in Google Form
•	Tagged in MC: Y
•	Package Sent: today's date
•	Note: the Zap I've set up currently only creates a new role and doesn't search for whether an individual already exists on the sheet
•	Trigger 2: Once an investor's subscription document has been fully executed via DocuSign (BOTH sets of signers have signed):
o	Upload a copy of the executed document to the individual's Google Drive folder (DocuSign emails me a copy when it is executed in my Outlook 365)
o	Update the individual's row on the Equity Sources Google Sheet, specifically populate the field below:
•	Docs Executed: Y
•	Trigger 3: Once the individual's wire transfer has been received (use email confirmation received from Axos Bank in my Outlook 365 account):
o	In MailChimp:
•	Copy the individual from the Prospective Investors audience to the Active audience (unless they're already in the Active audience)
•	Remove the "AEFI Subscribers" tag from their profile in the Prospective Investors audience
•	Add "AEFI Investors" tag to their profile in the Active audience
o	Send the Confirmation of Your Wire Email (see contents at the bottom of this document)
•	Note: since I only have the free version of MailChimp this will need to be done through an Outlook Zap rather than an Automation in Mailchimp
o	Send an email from me to transfer.agency@navconsulting.net with the individual's executed subscription document attached (details at the bottom of this document)
o	Update individual's row on the Equity Sources Google Sheet, specifically populate the field below:
•	Funds Received: today's date
o	Update individual's Lead record in ZohoCRM, fields to update are:
•	Company field to "Investors"
•	Lead Status field to "Pre-Qualified"
 
