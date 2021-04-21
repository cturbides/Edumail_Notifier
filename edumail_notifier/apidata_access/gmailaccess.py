#####################################################
#                                                   #
#                                                   #
#           CODE CREATED BY Ty4115 or Carlos        #
#                                                   #
#                                                   #
#####################################################

#Importing the packages for GmailAPI
from __future__ import print_function
import os.path
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def Gmail_CredentialsAccess():
    """
    Gets and return the credentials from a json file to access the API.
    If the json file doesn't exists, it creates it afer user grants the permision with
    his gmail account.
    """
    #If we modify these scopes, we had to delete the token.json file
    SCOPES = [  "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.labels",
                "https://www.googleapis.com/auth/gmail.modify"
             ]
    creds = None
    #The token file is created automatically. 
    #Sometimes we had to concede a user's access
    if os.path.exists('edumail_notifier/credentials/token.json'):
        creds = Credentials.from_authorized_user_file('edumail_notifier/credentials/token.json', SCOPES)
    #If there no valid credential available:
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                                                            'edumail_notifier/credentials/credentials.json', 
                                                            SCOPES
                                                            )
            creds = flow.run_local_server(port=0)
        # Saving the credentials for the next run
        with open('edumail_notifier/credentials/token.json', 'w') as token:
            token.write(creds.to_json())
    #Returning the credentials for use it in Gmail_InboxMailsReceived function
    return creds
            
            
def Gmail_InboxMailsReceived(creds):
    """
    It return a list of names of teachers who left a homework.
    Basically it take the last 8 mails received or located in INBOX and loop it. 
    If this particular mail also tagged UNREADED, it get the
    Subject and Sender of the mail. Analyze the Subject, looking if it is a homework,
    and if it's True, it return the name of the sender (if the teacher is from the classroom platform).  
    """
    
    #First we have to create a instance of a service builded (API build)
    SERVICE = build("gmail", "v1", credentials= creds)
    #Then we get unread messages body (id, name, messagesTotal, messagesUnreaded, etc)
    INBOX_BODY = SERVICE.users().labels().get(userId= 'me', id= 'INBOX').execute()
    
    #We have to know if we had unreaded messages
    UnreadedMessages = INBOX_BODY['messagesUnread']
    
    if UnreadedMessages:        
        #Getting the unreaded messages
        UNREADED_MESSAGES_BODY = SERVICE.users().messages().list(
                                                             userId= 'me',
                                                             maxResults= 8 #The last 8 mails received in INBOX 
                                                             ).execute()
        
        MESSAGES = UNREADED_MESSAGES_BODY.get('messages', [])

        try:
            sender_nameslist = [] #A list that are going to content the Email's sender name
            for msg in MESSAGES:
                #Get the message body (id, threadedId, labelIds, etc)
                txt = SERVICE.users().messages().get(
                                                    userId= 'me',
                                                    id = msg['id']
                                                    ).execute()
                try:
                    #Run the code if the message is unreaded
                    if 'UNREAD' in txt['labelIds']:
                        PAYLOAD = txt['payload'] #Refers to the mail body
                        HEADERS = PAYLOAD['headers'] #Refers to the mail header 
                    
                        #A loop to define the mail subject and sender
                        for sentence in HEADERS:
                            if sentence['name'] == 'Subject':
                                SUBJECT = sentence['value']
                            if sentence['name'] == 'From':
                                SENDER = sentence['value']
                
                        #print("Subject: ", SUBJECT)
                        #print("From: ", SENDER)
                  
                        #Now a loop for every word in the subject sentence
                        complete_sentence = ""
                
                        for word in SUBJECT.split():
                            complete_sentence += " " + word
                            if complete_sentence == " Nueva tarea:": #Modify this conditional sentence if its different
                                #Now a loop for every word in the sender sentence
                                for snt in SENDER.split("\""):                     
                                    if snt:
                                        snt = snt.split()
                                        if snt[-1] == "(Classroom)":#Modify this conditional sentence if it is other 
                                                                    #application or if the application name in the mail 
                                                                    #it's in a different position.
                                            
                                            sender_nameslist.append(' '.join(snt[0:len(snt)-1]))
                
                except Exception as e: #If an exception happend (in the second try block)
                  print(f'An exception occurred. {e}')
                    
            return sender_nameslist #If all goes right we return the email's sender names 

        except Exception as e: #If an exception happend (in the first try block)
            print(f'An exception occurred {e}')
    
    

if __name__ == "__main__":
    creds = Gmail_CredentialsAccess()
    Sender_name = Gmail_InboxMailsReceived(creds)
    print(Sender_name) #If all works, it will show the Email's Sender name