"""
    This code was developed by Hamza Abdalla as a part of the Chatbot project in the 
    NLP course during the automn semster 2020


"""
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from unidecode import unidecode
import numpy as np
import string


Similarity_Threshold = 0.7
index = 0

index_Stack = []


def pre_process_1(data):
    # convert input corpus to lower case.
    data = data.lower()
    # remove non-ascii characters
    data = unidecode(data)
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)

    # word_tokenize is used to tokenize the input corpus in word tokens.
    data = word_tokenize(data)
    # remove stop words and punctuations from string.
    filtered_sentence = [w for w in data if not w in stopset]
    filtered_sentence = [] 
    for w in data: 
        if w not in stopset:
            filtered_sentence.append(w) 
    
    data = filtered_sentence

    # commenting the lemmatization and stemming part prevent many problems while calculating the similarity

    # stripping affixes using Porter stemmer and WordNet lemmatizer
    # porter = nltk.PorterStemmer()
    # data = [porter.stem(t) for t in data]

    # wnl = nltk.WordNetLemmatizer()
    # data = [wnl.lemmatize(t) for t in data]

    #creating a new list contains the synsets of the words of the preprocessed data
    newData = []
    for w in data:
        newData.append(wn.synsets(w))

    # joining the newData list elements in a single list
    output = []
    for i in newData:
        for j in i:
            output.append(j)

    # print(output)
    
    return output

# the first method to calculate the simlarity between to sentences using the wordnet synsets and calculate a score
# based on the the path similarity and return the average of the "sumSimilarityscores" variable and return the average of
# similarity  

def Similarity_1(sent1, sent2):
    """
    Purpose: Computes sentence similarity using Wordnet path_similarity().
    Input: Synset lists representing sentence 1 and sentence 2.
    Output: Similarity score as a float
    """
    synsets1 = pre_process_1(sent1)
    synsets2 = pre_process_1(sent2)
    print("-----")
    print("Synsets1: %s\n" % synsets1)
    print("Synsets2: %s\n" % synsets2)
    
    sumSimilarityscores = 0
    scoreCount = 0
    
    # For each synset in the first sentence...
    for synset1 in synsets1:
    
        synsetScore = 0
        similarityScores = []
    
        # For each synset in the second sentence...
        for synset2 in synsets2:
        
            # Only compare synsets with the same POS tag. Word to word knowledge
            # measures cannot be applied across different POS tags.
            if synset1.pos() == synset2.pos():
            
                # Note below is the call to path_similarity mentioned above. 
                synsetScore = synset1.path_similarity(synset2)
    
                if synsetScore != None:
                    # print("Path Score %0.2f: %s vs. %s" % (synsetScore, synset1, synset2))
                    similarityScores.append(synsetScore)
    
                # If there are no similarity results but the SAME WORD is being
                # compared then it gives a max score of 1.
                elif synset1.name().split(".")[0] == synset2.name().split(".")[0]:
                    synsetScore = 1
                    # print("Path MAX-Score %0.2f: %s vs. %s" % (synsetScore, synset1, synset2))
                    similarityScores.append(synsetScore)
    
                synsetScore = 0
    
        if(len(similarityScores) > 0):
            sumSimilarityscores += max(similarityScores)
            scoreCount += 1
    avgScores = 0
    # Average the summed, maximum similarity scored and return.
    if scoreCount > 0:
        avgScores = sumSimilarityscores / scoreCount
    
    print("Func Score: %0.2f" % avgScores)
    return(avgScores)


# the second similarity method based on the WU & Palmer method that was presented in lab3
# the pre_process_2 function return a different data than pre_process_1 as pre_process_1 was based on returining 
# a list contains the synsets of the words of the passed sentence. but in preprocess_2 we return a list contains the 
# words of each sentence after doing the basic preprocessing

def pre_process_2(data):
    # convert input corpus to lower case.
    data = data.lower()
    # remove non-ascii characters
    data = unidecode(data)
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)

    # word_tokenize is used to tokenize the input corpus in word tokens.
    data = word_tokenize(data)
    # remove stop words and punctuations from string.
    filtered_sentence = [w for w in data if not w in stopset]
    filtered_sentence = [] 
    for w in data: 
        if w not in stopset:
            # w = wn.synsets(w) 
            filtered_sentence.append(w) 
    
    data = filtered_sentence
    return data

def wup(S1, S2):
    return S1.wup_similarity(S2)


# this function calcualte the similarity between two words usnig the WU & Palmer method
def word_similarity(w1,w2):
    #getting the most relative synset from the word
    if wn.synsets(w1) == None:
        return 0
    S1 = wn.synsets(w1)[0]
    S2 = wn.synsets(w2)[0]
    # print(w1,w2)
    # print(S1,'\n_________________\n',S2)
    if S1 and S2:
        # calculating the WU & palmer similarity between the two synsets if exist
        similarity = wup(S1, S2)
        if similarity:
          return round(similarity,2)
    return 0

# this function calculate the simlarity between two scentencs and return a float representing the value of this similarity
def Similarity_2(T1, T2):
    #preforme suitable preprocessing on each scentence
    words1 = pre_process_2(T1)
    words2 = pre_process_2(T2)
    
    tf = TfidfVectorizer(use_idf=True)
    tf.fit_transform([' '.join(words1), ' '.join(words2)])

    Idf = dict(zip(tf.get_feature_names(), tf.idf_))
    
    Sim = 0
    Sim_score1 = 0
    Sim_score2 = 0
    
    for w1 in words1:
        Max = 0
        if wn.synsets(w1) == None:
            continue
        for w2 in words2:
            if wn.synsets(w2) == None:
                continue
            # print(w1,w2)
            score = word_similarity(w1,w2)
            if Max < score:
               Max = score
        Sim_score1 += Max*Idf[w1]
    Sim_score1 /= sum([Idf[w1] for w1 in words1])
    
    
    for w2 in words2:
        Max = 0
        for w1 in words1:
            score = word_similarity(w1,w2)
            if Max < score:
               Max = score
        Sim_score2 += Max*Idf[w2]
        
    Sim_score2 /= sum([Idf[w1] for w2 in words2])
    

    Sim = (Sim_score1+Sim_score2)/2
    
    return round(Sim,2)


Res = ['Response one','Response Two','Response Three','Response Four','Response Five','Response sex']

T1 = 'Dogs are awesome.'
T2 = 'Some gorgeous creatures are awesome.'
T3 = 'Dolphins are swimming mammals.'
T4 = 'Cats are beautiful animals.'

# print('Similarity(T1, T2) =',Similarity(T1, T2))

History = {} # multi dimentional dictionary contains the the query-response of the session context
          # ex : { 0 : {query : (Response(S) )}}



def SearchContext(Query):
    for i in reversed(range(len(index_Stack))):
        for key,value in History[i].items():
            print(key + " --------- " + Query)
            sim = Similarity_1(key, Query)
            # sim = Similarity_2(key, Query)
            print('Similarity =', sim) 
            if sim >= Similarity_Threshold:
                return sim , i
                
        
    return 0,-1
            


def Agent_One(Query):
    global index
    global Response

    # if this is the first query in the session skip checking the context history because it's empty and forward the query to agent 2
    if index == 0: 
        History.setdefault(index,{})[Query] = Res[index]
        Response = Res[index]
        index_Stack.append(index)
        index += 1
    else :
        CalcSim, i = SearchContext(Query)
        if CalcSim :
            Response = Res[i]
        else:
            History.setdefault(index,{})[Query] = Res[index]
            Response = Res[index]
            index_Stack.append(index)
            index += 1
            

    # Response = 'Hello, I am Chatbot'
    for key, value in History.items():
        print(key , ":" , value)
        
    return Response

# for i in range(4):
#     Query = input("Enter the Query :")
#     Responce = input("Enter the Responce :")
#     test.setdefault(index,{})[Query] = Responce
#     index_Stack.append(index)
#     index += 1


# Agent_One(T1)
# Agent_One(T2)
# Agent_One(T3)
# Agent_One(T4)



# for i in range(len(test)):
#     for key,value in test[i].items():
#         print(key + " --------- " + T1)
#         print('Similarity(T1, T2) =',Similarity(key, T1))  

