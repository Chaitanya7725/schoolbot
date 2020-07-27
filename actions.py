# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
#
#


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!!!")

        return []


class ShowTopic(Action):

    def name(self) -> Text:
        return "show_topic"

    def run(self,dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

        conn = sqlite3.connect('history.db')
        user_message = str((tracker.latest_message)['text'])
        exe_str=''
        if "History" in user_message:
            exe_str = "Select id,topic from topics where subject is '{0}'".format('History')
        elif "Geography" in user_message:
            exe_str = "Select id,topic from topics where subject is '{0}'".format('Geography')
        elif "Science" in user_message:
            exe_str = "Select id,topic from topics where subject is '{0}'".format('Science')

        content = conn.execute(exe_str)
        content_text = ''
        for index,value in enumerate(content):
            content_text+=str(value[0]) + ") " +str(value[1]) + "\n"

        content_text+="\nPlease enter index. For eg, 1"
        dispatcher.utter_message(text=content_text)

        return []


class ManageResponse(Action):

    def name(self) -> Text:

        return "manage_response"

    def run(self,dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

        dispatcher.utter_message(text="I've noted your query. Please enter your email address")


class SendEmail(Action):

    def name(self) -> Text:
        return "send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect('history.db')
        messages = []
        exe_str = ''
        try:
            for event in tracker.events:
                if event.get("event") == "user":
                    messages.append("{}".format(event.get("text")))

            exe_str = "Select topic, link, page from topics where id is '{0}'".format(messages[-2])
            content1 = conn.execute(exe_str)
            for i in content1:
                context_text = str(i[0]) + " : " + str(i[1])

            # fromaddr = 'xyz@gmail.com'       ##Enter source email here
            print("1")
            # toaddrs = messages[-1]
            msg= EmailMessage()
            msg['Subject'] = 'School bot notification'
            msg['From'] = 'xyz@gmail.com'     ##Enter source email here 
            msg['To'] = messages[-1]
            msg.set_content("Hello student,\n\nFollowing is the resource requested by you. Best of luck :)\n" + context_text)
            username = 'xyz@gmail.com'      ##Enter username(Email) here

            obj = open('pass.txt')
            password = obj.read()
            print("2")
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(username, password)
                smtp.send_message(msg)

            # server = smtplib.SMTP('smtp.gmail.com:587')
            # server.ehlo()
            # server.starttls()
            print("3")
            # server.login(username, password)
            print("4")
            # server.sendmail(fromaddr, toaddrs, msg)
            # server.quit()
            print("5")
            dispatcher.utter_message(text="I've mailed you with the required resource. Please check")

        except:
            dispatcher.utter_message(text="Sorry system ran into trouble.. Can you please check again?")
