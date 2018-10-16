from flask import Flask, request, jsonify
import gspread  
from oauth2client.service_value_db import Servicevalue_dbCredentials
import json, requests
import http.client, urllib.request, urllib.parse, urllib.error, base64
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)

#Read
@app.route("/getvaluerow/<string:messenger_id>/<string:value_db>")
def getvaluerow(messenger_id, value_db):

	#Credentials to authorize the use of Google Excel Sheets and Google Drive services
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds =  Servicevalue_dbCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    #Use your previously created Google Excel Sheet
    sheet = client.open('<Name_of_your_Google_Excel_Sheet>').sheet1
    row = sheet.row_values(sheet.find(value_db).row)

    #Replace <BOT_ID>, <TOKEN> and <BLOCK_ID> by those from your Chatfuel Bot
    url2= "/bots/<BOT_ID>/users/"+messenger_id+"/send?chatfuel_token=<TOKEN>&chatfuel_block_id=<BLOCK_ID>"
    #Var Result will contain the second value of the row we have searched for
    data = {'Result': + int(row[1]) }
    headers = {'Content-type': 'application/json'}
    print(row[1])
    try:
      conn = http.client.HTTPSConnection("api.chatfuel.com")
      conn.request("POST", url2, json.dumps(data), headers)
      response = conn.getresponse()
      data = response.read()
      result = json.loads(data)
      print(result)
      print(data)
      conn.close()
    except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data

#Create
@app.route("/createrow/<messenger_id>/<value_db>")
def createrow(messenger_id,value_db):

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds =  Servicevalue_dbCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    sheet = client.open('<Name_of_your_Google_Excel_Sheet>').sheet1
    row = [messenger_id,value_db]

    sheet.append_row(row)

    return 'true'

#Update
@app.route("/updatevaluerow/<messenger_id>/<value_db>")
def updatevaluerow(messenger_id,value_db):

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds =  Servicevalue_dbCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    sheet = client.open('<Name_of_your_Google_Excel_Sheet>').sheet1
    all_rows = sheet.get_all_records()

    row_id_list = []
    row_value_list = []
    messenger_id_list = []

    row_real_id_list = [] #indices increased by 2 

    for idx, row in enumerate(all_rows):
        row_id_list.append(idx)
        row_value_list.append(row)
        messenger_id_list.append(row['ID'])
    for idx in row_id_list:
        row_real_id_list.append(idx+2)
    #dictonary is composed of the index of the row in google sheet (increased by 2) and messenger id
    dictionary = dict(zip(row_real_id_list, messenger_id_list))
    for rowid, messengerid in dictionary.items():
        if str(messengerid) == str(messenger_id):
            index_row_to_update = rowid
            sheet.update_cell(index_row_to_update, 2, value_db)
            return 'true'

#Delete
@app.route("/deleterow/<messenger_id>")
def deleterow(messenger_id):
	åå
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds =  Servicevalue_dbCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    sheet = client.open('<Name_of_your_Google_Excel_Sheet>').sheet1
    all_rows = sheet.get_all_records()

    row_id_list = []
    row_value_list = []
    messenger_id_list = []

    row_real_id_list = [] #indices increased by 2 

    for idx, row in enumerate(all_rows):
        row_id_list.append(idx)
        row_value_list.append(row)
        messenger_id_list.append(row['ID'])
    for idx in row_id_list:
        row_real_id_list.append(idx+2)
    #dictonary is composed of the index of the row in google sheet (increased by 2) and messenger id
    dictionary = dict(zip(row_real_id_list, messenger_id_list))
    for rowid, messengerid in dictionary.items():
        if str(messengerid) == str(messenger_id):
            index_row_to_update = rowid
            sheet.update_cell(index_row_to_update, 1, -1)
            sheet.update_cell(index_row_to_update, 2, -1)
            return 'true'


#Send an email
@app.route("/sendemail/<emailaddr>")
def send_email(emailaddr):

    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    #Email and Password of the sender
    username = '<your_email_address>'
    password = '<your_email_pw>'
    sender = '<your_email_address>'
    #Email of the receiver
    targets = [emailaddr]

    msg = MIMEText('<your_email_text>')

    msg['Subject'] = '<your_email_subject>'
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()
    return 'true'

 
if __name__ == "__main__":
    app.run()