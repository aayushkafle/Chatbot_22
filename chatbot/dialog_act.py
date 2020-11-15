import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import joblib

class dialog_act_classifier:
    def __init__(self, classifier="SVM", feature="tfidf"):
        
        if classifier not in ["SVM", "RandomForest"]:
            print("select either SVM or RandomForest")
        
        if feature not in ["tfidf", "BOW"]:
            print("select either tfidf or BOW")
        
        dataset = dataset = pd.read_csv("others/dataset.csv").set_index("Unnamed: 0")
        
        if feature == "tfidf":
            self.vectorizer = TfidfVectorizer()
        
            if classifier == "SVM":
                model_file = "models/svc_tfidf.pkl"
        
            elif classifier == "RandomForest":
                model_file = "models/rf_tfidf.pkl"
        
        elif feature == "BOW":
            self.vectorizer = CountVectorizer()
        
            if classifier == "SVM":
                model_file = "models/svc_BOW.pkl"
        
            elif classifier == "RandomForest":
                model_file = "models/rf_BOW.pkl"

        self.vectorizer.fit(dataset["cleaned_utterance"])
        self.classifier_model = joblib.load(model_file)

        self.dialog_dictionary = pd.read_csv("others/dialog_dictionary.csv").set_index("dialog_acts")

    def transform(self, text):
        return self.vectorizer.transform([text])
    
    def predict(self, data):
        return self.classifier_model.predict(data)

    def transform_predict(self, text):
        return self.predict(self.transform(text))

    def description_reply(self, dialog_act):
        result = {"class": dialog_act[0], "Description":self.dialog_dictionary["Description"][dialog_act[0]], "Response":self.dialog_dictionary["response"][dialog_act[0]]}
        return result

    def full_result(self, text):
        return self.description_reply(self.transform_predict(text))    

if __name__=="__main__":
    dac = dialog_act_classifier()
    query = "Thank you"
    print(query)
    response = dac.full_result(query)
    print(response)
    if pd.isnull(response["Response"]):
        print("Nan detected")
    # dac.predict(dac.transform("thank you"))