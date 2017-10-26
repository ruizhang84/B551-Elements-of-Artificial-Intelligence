#!/usr/bin/python
import sys
import math
import heapq

class Entry:
    """ 
        A class to handle input/output data,
        including city, tweet content
    """
    def __init__(self, location, entry):
        self.location = location
        self.entry = entry
        self.word_list = set()

    def update_word(self, token):
        self.word_list.add(token)
        return


class Vector:
    """
        A class to help get prob
        includes city, the number of words in tweet
        
        location is the place to label like Chicago
        bag_of_words is a hash fuction from token -> frequence
    """
    def __init__(self, location):
        self.location = location
        self.temp_words = {}
        self.words = {}

    def update_word(self, token):
        if token not in self.temp_words:
            self.temp_words[token] = 0
        self.temp_words[token] += 1
        return
        
    def adjust_word(self, word_dict):
        # add extra 1 to count for zero probability
        self.words = {}
        for token in word_dict:
            if token not in self.temp_words:
                self.words[token] = 1
        for token in self.temp_words:
            self.words[token] = self.temp_words[token] + 1
        return


class Data:
    """
        A class to handle the data set 
        including all entires, vectors and locations

        entry -- all the tweet line
        location -- the number of loctions in train
        word_dict -- the words appears in word
        vector -- the vector to calculate prob
    """
    def __init__(self):
        self.entry = []
        self.location = {}
        self.word_dict = set()
        self.vectors = {}

    def update_entry(self, entry):
        self.entry.append(entry)
        return

    def update_location(self, city):
        if city not in self.location:
            self.location[city] = 0
        self.location[city] += 1
        return

    def update_words(self, token):
        self.word_dict.add(token)
        return

    def update_vectors(self, vector):
        location = vector.location
        if location not in self.vectors:
            self.vectors[location] = vector
        return

def process_data(file):
    def process_line(line):
        line = line.strip()
        return line.split(" ")

    data_set = Data()
    with open(file, 'r') as f:
        for line in f:
            record = line.strip()
            temp = process_line(line)
            location = temp[0]
            temp = temp[1:]
            
            entry = Entry(location, record)
            vector = Vector(location)
            if location in data_set.vectors:
                vector = data_set.vectors[location]
            for token in temp:
                vector.update_word(token)
                entry.update_word(token)
                data_set.update_words(token)
            
            data_set.update_entry(entry)
            data_set.update_vectors(vector)
            data_set.update_location(location)
            
    return data_set


class Prob:
    """
        A class to calculate probability,
        P(city | words) = P(words | city) * p(city) / p(words)
    """
    def __init__(self, city_name):
        self.city = city_name
        self.cond_prob = {}
        self.prior_prob = 0
    
    def update_cond_prob(self, train_set, test_set):
        total = 0
        vector = train_set.vectors[self.city]
        vector.adjust_word(test_set.word_dict)
        for token in vector.words:
            total += vector.words[token]
        for token in vector.words:
            prob = vector.words[token] * 1.0 / total
            self.cond_prob[token] = -math.log(prob)
        return

    def update_prior_prob(self, train_set):
        total = 0
        for city in train_set.location:
            total += train_set.location[city]
    
        prob = train_set.location[self.city] * 1.0 / total
        self.prior_prob =  -math.log(prob)
        return

class Classifer:
    """
        A class to compute the navie bayes
        naive bayes assumption
        P(city | words) = P(words | city) * p(city) / p(words)
                        = p(w1|city)p(w2|city)... * p(city)
                        (ignore the prior of words) 
    """
    def __init__(self):
        self.prob = {}

    def update_prob(self, prob):
        self.prob[prob.city] = prob

    def prob_predict(self, word_list):
        # argmax
        # P(city | words) = p(city) * \pi{ p(wi | city) }
        min_prob = float("inf")
        candid = None
        for city in self.prob:
            prob = self.prob[city]
            temp = prob.prior_prob
            for token in word_list:
                temp += prob.cond_prob[token]
            if temp < min_prob:
                min_prob = temp
                candid = city
        return candid    

def naive_bayes(train_set, test_set):
    """
        naive bayes assumption
        P(city | words) = P(words | city) * p(city) / p(words)
                        = p(w1|city)p(w2|city)... * p(city)
                        (ignore the prior of words)
    """
    classifer = Classifer()

    for city in train_set.location:
        prob = Prob(city)
        prob.update_cond_prob(train_set, test_set)
        prob.update_prior_prob(train_set)
        classifer.update_prob(prob)

    return classifer


def predict_test(output_file, test_set, classifer):
    result = []
    with open(output_file, 'w') as f:
        for record in test_set.entry:
            # bayes classifer
            estimate = classifer.prob_predict(record.word_list)
            output = estimate + ' ' + record.entry + '\n'
            f.write(output)
            result.append((estimate, record.entry))
    return result

class Top:
    """
        A class to handle top five words 
        associate with city
    """
    def __init__(self, city):
        self.city = city
        self.actual = None
        self.word_count = {}

    def update_word(self, entry):
        words = entry.split(" ")
        self.actual = words[0]
        words = words[1:] # skip first token
        for token in words:
            if token not in self.word_count:
                self.word_count[token] = 0
            self.word_count[token] += 1
        return

    def top_five(self):
        temp = sorted(self.word_count, key=self.word_count.get, reverse=True)
        return temp[:5]


def top_five(result):
    top_words = {}
    correct = 0
    for (city, entry) in result:
        if city not in top_words:
            top_words[city] = Top(city)
        name = entry.split(" ")[0]
        if name == city:
            correct += 1
        top_words[city].update_word(entry)
    for city in top_words:
        print city,
        for word in top_words[city].top_five():
            print word,
        print
    #print "accuracy: ", correct*1.0/len(result)
    return

# ###########################
assert(len(sys.argv)) == 4
prog, train_file, test_file, output_file = sys.argv
#train_file = "tweets.train.txt"
#test_file = "tweets.test1.txt"
#output_file = "temp.txt"

# read in data
train_set = process_data(train_file)
test_set = process_data(test_file)

# process data
classifer = naive_bayes(train_set, test_set)

# make prediction
result = predict_test(output_file, test_set, classifer)

# print out output
top_five(result)
            


