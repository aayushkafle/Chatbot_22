import requests
import json
import pandas as pd

from chatbot.dialog_act import dialog_act_classifier
from chatbot.clones import response, special_intent
from chatbot.agent3v1_1_2 import agent3

class agent2:
    def __init__(self, clone_name, rasa_url="http://localhost:5005/model/parse"):
        self.dac = dialog_act_classifier()
        self.rasa_url = rasa_url
        self.fallback_msg = "I cannot understand your statement, please rephrase it"
        self.threshold = 0.7
        self.clone_name = clone_name

    def classify_dialog(self, text):
        return self.dac.full_result(text)

    def rasa_query(self, text):
        msg = requests.post(self.rasa_url, json.dumps({"text":text}))
        if msg.status_code == 200:
            intent = json.loads(msg.text)["intent"]["name"]
            confidence = json.loads(msg.text)["intent"]["confidence"]
            if confidence >= self.threshold:
                return intent, 1
            else:
                return self.fallback_msg, 0
        else:
            return "RASA server Error code, " + msg.status_code, 0

    def classify_intent(self, text):
        dialog_act = self.classify_dialog(text)
        if pd.isnull(dialog_act["Response"]):
            intent, status = self.rasa_query(text)
            if not status:
                return intent, "error", "error"
            if intent in special_intent:
                if intent == "google":
                    ag3, url = agent3(text)
                    if len(ag3) == 0:
                        ag3 = "Error in google search"
                    return ag3 + "view more at the following link: " + url, dialog_act["class"], intent
                else:
                    return "Sorry, I cannot execute the command right now. Will do it in the next update", dialog_act["class"], intent
            else:
                return response[self.clone_name][intent], dialog_act["class"], intent        
        else:
            return dialog_act["Response"], dialog_act["class"], False

if __name__=="__main__":
    a2 = agent2("cafe")
    print(a2.classify_intent("Who is GPS coordinate? "))