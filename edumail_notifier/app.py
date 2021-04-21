"""

-------------------------------------------------------------------------------------------
                        THIS CODE WAS CREATED BY Ty4115 or Carlos
-------------------------------------------------------------------------------------------
    
"""

from edumail_notifier.apidata_access import gmailaccess
from edumail_notifier.showing_apidata import notifier
import time


def run():
    """
    It return a notification if there are homeworks left (thanks to mails of classroom in the email).
    And is executing continously itself as a recursive object. 
    """
    creds = gmailaccess.Gmail_CredentialsAccess() #Credentials for API access.
    SenderListNames = gmailaccess.Gmail_InboxMailsReceived(creds) #Passing the credentials through the script that
                                                                   #return a list with the mail senders (in this case,
                                                                   #the teachers who leave homework).
    if SenderListNames: #If senderList isn't null.
        for name in SenderListNames: #For every new homework is going to send a notification.
            Popup_Notifier = notifier.Notification(
                                                    title= "Tarea de Classroom",
                                                    message= f"Tienes una nueva tarea de {name}",
                                                    icon_path= "edumail_notifier/resources/Edumail_icon.ico",
                                                    application_name= "EduMail",
                                                    sound= "edumail_notifier/resources/samsung_charming_bell.wav"
                                                  )
            Popup_Notifier.Send_Notification()
    time.sleep(100) #The script will wait 100 seconds to run itself again.
    run()

