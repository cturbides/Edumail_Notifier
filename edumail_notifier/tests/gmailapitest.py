#Importing needed packages and modules
from __future__ import print_function
import os.path
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64

#This function return in a correct syntax a label for a Gmail Email
def makes_labels(name, mLv = "show", llv = "labelShow"):
    label = {
            "messageListVisibility": mLv,
            "labelListVisibility": llv,
            "name": name        
            }    
    return label


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.modify']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('edumail_notifier/credentials/token.json'):
        creds = Credentials.from_authorized_user_file('edumail_notifier/credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'edumail_notifier/credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('edumail_notifier/credentials/token.json', 'w') as token:
            token.write(creds.to_json())
    
    #API Request
    service = build("gmail", "v1", credentials=creds)
    
    
    #get labels
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels",[])
       
    
    """
    #Create a Label
    try:
        label = makes_labels("Test_1")
        created_label = service.users().labels().create(userId="me", body= label).execute()
        print("Label created, watch your Gmail")
    except Exception as e:
        print(f'An exception occurred. {e}')
    """
    
    """
    #Delete a Label
    try:
        last_labelId = labels[-1]["id"]
        deleteLabel = service.users().labels().delete(userId="me", id=last_labelId).execute()
        print("That's Label was deleted. Check your Gmail")
    except Exception as e:
        print(f'An exception occurred. {e}')
    """
    
    #Read the Inbox's Messages
    result = service.users().messages().list(userId= "me", maxResults= 15).execute()
    messages = result.get("messages",[])
    try:
        for msg in messages:
            txt = service.users().messages().get(userId="me", 
                                                 id=msg["id"]                                                      
                                                ).execute()
            try:
                payload = txt["payload"]
                headers = payload["headers"]
              
                for d in headers:
                    if d["name"] == 'Subject':
                        subject = d['value']
                    if d['name'] == "From":
                        sender = d['value']
                                        
                print("Subject: ", subject)
                print("From: ", sender)
                print("\n")
            
            except Exception as e:
              print(f"There's a problem: {e}")
              
    except Exception as e:
      print(f'An exception occurred. {e}')    
      
        
if __name__ == '__main__':
    main()