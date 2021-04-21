#####################################################
#                                                   #
#                                                   #
#           CODE CREATED BY Ty4115 or Carlos        #
#                                                   #
#                                                   #
#####################################################

#Importing package for the notifier
from notifypy import Notify

class Notification:
    """
    When an object of this class is created and is used the Send_Notification method, it send a notification
    with detailed parameters.
    """
    #Creating the init method with defaullt values if user didn't send them
    def __init__(self, title = "That's the title", message = "That's the message", icon_path = "edumail_notifier/resources/icon-people-circle.ico", 
                 application_name = "Python", sound = "edumail_notifier/resources/samsung_bubbles.wav"):
        
        self.title = title
        self.message = message
        self.icon_path = icon_path
        self.application_name = application_name
        self.sound = sound
        
        self.notification = Notify()
        self.notification.title = self.title
        self.notification.message = self.message
        self.notification.application_name = self.application_name
        self.notification.icon = self.icon_path
        self.notification.audio = self.sound 
    
    def Send_Notification(self):
        self.notification.send()

if __name__ == "__main__":
    Pop = Notification()
    Pop.Send_Notification()
