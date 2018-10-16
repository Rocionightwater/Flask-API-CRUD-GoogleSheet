# README

In order to work with Google Sheets you will have to create certain permissions. You will also need to create the files client_secret.json, Procfile and have a requirements.txt file (pip freeze > requirements.txt). 

### This video explains very well how to get the permissions and how to create these files:
https://www.youtube.com/watch?v=vISRn5qFrkM

## CRUD operations

This API is ready to work with the chatbots platform Chatfuel.
Chatfuel Broadcasting API looks like this:

https://api.chatfuel.com/bots/<BOT_ID>/users/<USER_ID>/send?chatfuel_token=<TOKEN>&chatfuel_message_tag=<CHATFUEL_MESSAGE_TAG>&chatfuel_block_name=<BLOCK_NAME>&<USER_ATTRIBUTE_1>=<VALUE_1>&<USER_ATTRIBUTE_2>=<VALUE_2>

### Source:
https://docs.chatfuel.com/api/broadcasting-api/broadcasting-api

- Input the name of your Google Excel Sheet in <Name_of_your_Google_Excel_Sheet>.

The Google Excel Sheet used in this API contains 2 columns composed of <messenger_id> and <value_db>; both are numbers that are created from the chatbot and sent to the google sheet by the CREATE operation. But NOTE that <messenger_id> in READ operation must be your own Facebook ID, otherwise the Broadcasting API call will not work properly.


- Input your Chatfuel Bot ID in <BOT_ID>
- Input your Chatfuel Bot Token in <TOKEN_ID>
- Input your Chatfuel Block ID in <BLOCK_ID> (This is the block where the user will be redirected to, in order to receive the value we are looking for in the google sheet)

## Send email operation

- Input your sender email address in <your_email_address>
- Input your sender email password in <your_email_pw>
- Input your email content in <your_email_text>
- Input your email subject in <your_email_subject>
- The receiver will be the one we pass as an parameter (parameter emailaddr)



