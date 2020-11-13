import pandas as pd
dataset = pd.read_csv("dataset.csv").set_index("Unnamed: 0")

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

bags_of_words = CountVectorizer().fit_transform(dataset["cleaned_utterance"])
# bags_of_words = CountVectorizer(stop_words="english", max_features=100).fit_transform(dataset["cleaned_utterance"])
# tfidf = TfidfVectorizer().fit_transform(dataset["cleaned_utterance"])


X_train_BOW, X_test_BOW, y_train_BOW, y_test_BOW = train_test_split(bags_of_words, dataset["Dialog_Act"], test_size = 0.2, random_state = 42, shuffle = True)

from sklearn import svm
svc_BOW = svm.SVC(kernel='linear')
# svc_tfidf = svm.SVC(kernel='linear')

svc_BOW.fit(X_train_BOW, y_train_BOW)
predictions_BOW = svc_BOW.predict(X_test_BOW)
print(classification_report(y_test_BOW, predictions_BOW))