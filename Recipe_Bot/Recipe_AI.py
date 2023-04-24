import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import sys
import os
from itertools import chain, combinations
sys.path.insert(0,'Recipe_Bot/')



class Model:
    def __init__(self):
        pass

    def run(self,make_model=False):
        print(os.getcwd())

        with open("Recipe_Bot/Food.json") as file:
            self.data = json.load(file)
        
        try:
            with open("Recipe_Bot/data.pickle", "rb") as f:
                self.words, self.labels, training, output = pickle.load(f)
        except:
            self.words = []
            self.labels = []
            docs_x = []
            docs_y = []
        
            for intent in self.data["intents"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    self.words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent["tag"])
        
                if intent["tag"] not in self.labels:
                    self.labels.append(intent["tag"])
        
            self.words = [stemmer.stem(w.lower()) for w in self.words if w != "?"]
            self.words = sorted(list(set(self.words)))
        
            self.labels = sorted(self.labels)
        
            training = []
            output = []
        
            out_empty = [0 for _ in range(len(self.labels))]
        
            for x, doc in enumerate(docs_x):
                bag = []
        
                wrds = [stemmer.stem(w.lower()) for w in doc]
        
                for w in self.words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)
        
                output_row = out_empty[:]
                output_row[self.labels.index(docs_y[x])] = 1
        
                training.append(bag)
                output.append(output_row)
        
        
            training = numpy.array(training)
            output = numpy.array(output)
        
            with open("data.pickle", "wb") as f:
                pickle.dump((self.words, self.labels, training, output), f)
        
        tensorflow.compat.v1.reset_default_graph()
        
        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)
        
        self.model = tflearn.DNN(net)
        
        # End of Setup
        
        if make_model==False:
            self.model.load("Recipe_Bot/model.tflearn")
        else:
            self.model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
            self.model.save("Recipe_Bot/model.tflearn")
        
        # End of Train/Load
    
    def bag_of_words(self,s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
                
        return numpy.array(bag)
    
    def powerset(self,iterable):
        s=list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    
    def find_combos(self,inp):
        all_combos=[]
        for i, combo in enumerate(self.powerset(inp),1):
            all_combos.append(combo)
        return all_combos


    def chat(self,not_self,inp=["egg"]):
        answer=[]   
        combos=self.find_combos(inp)
        
        for i in range(len(combos)):
            ing=""
            for j in range(len(combos[i])):
                if j==0:
                    ing=combos[i][j]
                elif j<len(inp)-1:
                    ing=ing+" and "+combos[i][j]
                else:
                    ing=ing+" "+combos[i][j]
                    
            not_self.text_event(f"Combo: {ing}")

            results = self.model.predict([self.bag_of_words(ing, self.words)])[0]
            results_index = numpy.argmax(results)
            tag = self.labels[results_index]
            # print(tag)
            if results[results_index] > 0.9:
                for tg in self.data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
                        break
                
                for response in responses:
                    answer.append([response['recipe_name'],response['ingredients'],response['condiments'],response['link']])
                    
            else:
                not_self.text_event("Nothing found")
        print(answer)
        return answer
