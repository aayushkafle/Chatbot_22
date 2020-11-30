from gensim import corpora, models
from pprint import pprint
import nltk
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import pandas as pd
import requests
import string
# from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup


def agent3(query):    
    ## TODO implement multi-agent system, including message3

    ## get relevant information from message3:
    # query = message3.get_query()
    # context = message3.get_context()

    # query = 'what is the height of ronaldo?'
    print('query: ' + query)

    context = 'band explain invite protagonist drug addiction alcohol sex hospital{0: {\'Dogs are awesome.\': \'Response one\'}, 1: {\'Dolphins are swimming mammals.\': \'Response Two\'}, 2: {\'Cats are beautiful animals.\': \'Response Three\'}}'
    #print('context: ' + context)

    # information retrieval with google search


    def chatbot_query(query, size=1):
        # This function performs google search on the query and then retrieves the output html documents. 
        # Then, it filters out the content of the htmls and returns the resulting documents as a list.

        fallback = 'Sorry, I cannot think of a reply for that.'
        resultlist = []
        articlelist = []

        try:
            search_result_list = list(search(query, tld="fi", num=10, stop=size, pause=1))

            for i in range(0, size):
                page = requests.get(search_result_list[i])

                # tree = html.fromstring(page.content)

                soup = BeautifulSoup(page.content, features="lxml")

                article_text = ''
                article = soup.findAll('p')
                for element in article:
                    article_text += '\n' + ''.join(element.findAll(text=True))
                article_text = article_text.replace('\n', '')
                first_sentence = article_text.split('.')
                first_sentence = first_sentence[0].split('?')[0]

                chars_without_whitespace = first_sentence.translate(
                    {ord(c): None for c in string.whitespace}
                )

                if len(chars_without_whitespace) > 0:
                    result = first_sentence
                else:
                    result = fallback
                resultlist.append(result)
                articlelist.append(article_text)
            return articlelist, search_result_list  # instead of resultlist
        except:
            # if len(result) == 0:
            result = [fallback]
            return result

    # actually performing google search and printing the results
    # print('\nperforming google search...')
    # print('results:')
    documents, search_result_list = chatbot_query(query, size=10)
    # for r in documents:
    #     print(r)

    # transforming to pandas DataFrame
    print('\ntransforming to pandas DataFrame')
    resultlist = pd.DataFrame(documents, columns=['a'])
    # print(resultlist.head(10))

    # resultlist = resultlist.dropna()
    # resultlist = resultlist[resultlist['a'].map(len)>0]
    # print(resultlist.head(10))

    # resultlist.to_csv("test.txt")

    # importing gensim and nltk
    np.random.seed(2018)

    print()
    nltk.download('wordnet')
    print()

    stemmer = SnowballStemmer('english')

    def lemmatize_stemming(text):
        # First lemmatizes the text and then stems it using SnowballStemmer.
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    def preprocess(text):
        # Removes stopwords, then uses lemmatize_stemming(text) on the text.
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(lemmatize_stemming(token))
        return result

    # preprocess the data
    # print('preprocess data: lemmatize and stem...')
    # print('result:')
    processed_docs2 = resultlist['a'].map(preprocess)
    processed_docs2

    # create a dictionary
    dictionary2 = gensim.corpora.Dictionary(processed_docs2)

    # The following outcommented code showed an extracted from the dictionary. For testing purposes.
    # print('extract from the dictionary:')
    # count = 0
    # for k, v in dictionary2.iteritems():
    #     print(k, v)
    #     count += 1
    #     if count > 10:
    #         break

    # filter out words that are contained in more than half of the documents
    dictionary2.filter_extremes(no_above=0.5)

    #
    bow_corpus2 = [dictionary2.doc2bow(doc) for doc in processed_docs2]
    # print('preview bag of words for document 8 as an example:')
    # print(bow_corpus2[7])

    # print('to better explain:')
    # bow_doc_7 = bow_corpus2[7]

    # for i in range(len(bow_doc_7)):
    #     print("Word {} (\"{}\") appears {} time.".format(bow_doc_7[i][0], 
    #                                                      dictionary2[bow_doc_7[i][0]], 
    #                                                      bow_doc_7[i][1]))

    # tfidf


    tfidf2 = models.TfidfModel(bow_corpus2)
    corpus_tfidf2 = tfidf2[bow_corpus2]
    # for doc in corpus_tfidf2:
    #     #pprint(doc)
    #     break

    # lda using bag of words
    # print('\nperforming lda using bag of words, specification: 10 topics')
    # print(bow_corpus2)
    lda_model2 = gensim.models.LdaMulticore(bow_corpus2, num_topics=10, id2word=dictionary2, passes=2, workers=3)
    # for idx, topic in lda_model2.print_topics(-1):
        # print('Topic: {} \nWords: {}'.format(idx, topic))

    # print('performing lda using tfidf, specification: 10 topics')
    # lda_model_tfidf2 = gensim.models.LdaMulticore(corpus_tfidf2, num_topics=10, id2word=dictionary2, passes=2, workers=4)
    # for idx, topic in lda_model_tfidf2.print_topics(-1):
    #     print('Topic: {} Word: {}'.format(idx, topic))

    # print('\n########')
    # print('quick look at bag of words of document 6 as an example:')
    # print(bow_corpus2[5])

    # print('\nhow well document 6 fits to the topics, in descending order:')
    # for index, score in sorted(lda_model2[bow_corpus2[4]], key=lambda tup: -1*tup[1]):
    #     print("\nScore: {}\t \nTopic: {}".format(score, lda_model2.print_topic(index, 10)))

    # print('########')
    # print()

    # for index, score in sorted(lda_model_tfidf2[bow_corpus2[4]], key=lambda tup: -1*tup[1]):
    #     print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf2.print_topic(index, 10)))

    # heuristic to match query to topics
    preprocessed_query = preprocess(query)
    # print('preprocessed query: ')
    # print(preprocessed_query)

    # preprocessing context history
    context = preprocess(context)
    # context

    # compute jaccard similarity between query and topics, store results in similarities[0]
    # then compute jaccard similarity between context and topics, store results in similarities[1]
    similarities = [[],[]]
    print()
    # print('compute jaccard similarities...')
    for i in range(0, len(lda_model2.show_topics())):
        words_in_topic = []
        topic = lda_model2.show_topics()[i][1]
        # print('\ntopic: ' + topic)
        current_word = ''
        for c in topic:
            if(c.isalpha()):
                current_word += c
            else:
                if(not current_word == ''):
                    words_in_topic.append(current_word)
                current_word = ''
        # print(words_in_topic)
        intersection = len(set(words_in_topic).intersection(preprocessed_query))
        union = (len(words_in_topic) + len(preprocessed_query)) - intersection
        f = intersection / union
        similarities[0].append(f)
        # print('jacsim of current topic with query: ' + str(f))
        intersection = len(set(words_in_topic).intersection(context))
        union = (len(words_in_topic) + len(context)) - intersection
        f = intersection / union
        similarities[1].append(f)
    #     print('jacsim of current topic with context: ' + str(f))
    # print('#################')
    # print('output similarities:')
    # print(similarities)

    def topic_choice_heuristic():
    # This is a heuristic for selecting the document that is most fitting for the user. 
    # It uses the jaccard similarities between the topics and the query or the context history, respectively.
    # It checks if the jacsim with the query is nonzero somewhere, if yes, it compares and 
    # choose the topic with the highest jacsim. 
    # If the jacsim with the query is zero it compare jacsims of the context history and parallely, takes the highest one.
    # If somewhere in the process multiple topics have the same jacsim, the one first in the list of topics is chosen.
    # Similarly, if both jacsim lists are full of zeros, the one first in the list of topics is chosen.
        highest_topic_index = -1
        max_sim = max(similarities[0])
        if(max_sim != 0):
            for i in range(len(similarities[0]) - 1, -1, -1):
                if(similarities[0][i] == max_sim):
                    highest_topic_index = i
        else:
            max_sim = max(similarities[1])
            if(max_sim != 0):
                for i in range(len(similarities[1]) - 1, -1, -1):
                    if(max_sim - 0.0000005 < similarities[1][i] < max_sim + 0.0000005):
                        highest_topic_index = i
            else:
                highest_topic_index = 0
        #   print('\nindex of highest jacsim: \n' + str(highest_topic_index))
        return highest_topic_index

    chosen_index = topic_choice_heuristic()

    def get_document_from_topic(chosen_index):
        # loop through documents, find document that is most fitting to the chosen topic
        highest_score = 0
        best_doc = -1
        # print('\n#######################')
        # print('loop through documents, find most fitting one for topic index ' + str(chosen_index))
        # print('Initializing: highest score: ' + str(highest_score))
        for i in range(0, 10):
            # print('\n--document index ' + str(i))
            for index, score in sorted(lda_model2[bow_corpus2[i]], key=lambda tup: -1*tup[1]):
                if(index == chosen_index and score > highest_score):
                    highest_score = score
                    best_doc = i
                    print('Highest score got updated!')
            #     print("\nScore: {}\t \nTopic: {}".format(score, lda_model2.print_topic(index, 10)))
            #     print('Topic id: ' + str(index))
            #     print('Highest score: ' + str(highest_score))
            #     print('best doc: ' + str(best_doc))
            # print('********************')
            # print('********************')
            # print('********************')
        return best_doc

    best_doc = get_document_from_topic(chosen_index)

    # print()
    # print('*************')
    # print()
    # print('*************')
    # print()
    # print('*************')

    print('The ' + str(best_doc+1) + '. document will be sent back to agent 2:')
    # print(documents[best_doc])
    if len(documents[best_doc])>100:
        return documents[best_doc][:50], search_result_list[best_doc]
    else:
        return documents[best_doc], search_result_list[best_doc]
