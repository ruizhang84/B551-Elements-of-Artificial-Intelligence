from sklearn.decomposition import PCA
import random, math, itertools
import numpy as np

MAX_CLASSIFER = 20
MAXITER = 200
THRESHOLD = 0
VECTOR = [i for i in range(192)]
random.seed(0)
OUTPUT = "output.txt"

def phaser_txt(fname):
    dataset = []
    with open(fname, 'r') as f:
        for line in f:
            record = line.strip().split(" ")
            photo_id, orient = record[:2]
            orient = int(orient)/90
            pixel = [int (i) for i in record[2:]] 
            dataset.append((photo_id, orient, pixel))
    return dataset

def display(record, fname):
    with open(fname, 'w') as f:
        for entry in record:
            photo_id, label = entry
            output = photo_id + " " + str(label*90) + "\n"
            f.write(output)
    return

def adaBoostModel(fname, classifer_arr):
    with open(fname, 'w') as f:
        for classifer in classifer_arr:
            output = []
            output.append(str((classifer.p1, classifer.p2)))
            output.append(str((classifer.p3, classifer.p4)))
            output.append(str((classifer.p5, classifer.p6)))
            output.append(str(classifer.label1))
            output.append(str(classifer.label2))
            output.append(str(classifer.label3))
            output.append(str(classifer.label4))
            output.append(str(classifer.weight))
            f.write("$".join(output)+ "\n")
    return

def loadAdaBoostModel(fname):
    classifer_arr = []
    with open(fname, 'r') as f:
        for line in f:
            pair1, pair2, pair3, label1, label2, label3, label4, weight = line.strip().split("$")

            temp = pair1[1:-1].split(',')
            pair1 = (int(temp[0]), int(temp[1]))
            temp = pair2[1:-1].split(',')
            pair2 = (int(temp[0]), int(temp[1]))
            temp = pair3[1:-1].split(',')
            pair3 = (int(temp[0]), int(temp[1]))

            label1 = int(label1)
            label2 = int(label2)
            label3 = int(label3)
            label4 = int(label4)

            weight = float(weight)
            classifer = Classifer(pair1, pair2, pair3, weight)
            classifer.label1 = label1
            classifer.label2 = label2
            classifer.label3 = label3
            classifer.lable4 = label4
            classifer_arr.append(classifer)
    return classifer_arr

class Classifer:
    """
        compare a pixel at one position to the another pixel value at some position.
        decide what color mostly likely to be
    """
    def __init__(self, pair1, pair2, pair3, weight=1.0/MAX_CLASSIFER):
        self.p1, self.p2 = pair1
        self.p3, self.p4 = pair2
        self.p5, self.p6 = pair3
        self.label1 = self.label2 = self.label3 = self.label4 = 0
        self.weight = weight
    
    def predict(self, img):
        if decision(img, self.p1, self.p2):
            if decision(img, self.p3, self.p4):
                return self.label1
            else:
                return self.label2
        else:
            if decision(img, self.p5, self.p6):
                return self.label3
            else:
                return self.label4
        return 0


###########################
# decision stumps
def decision(img, p1, p2):
    return img[p1] - img[p2] > THRESHOLD

def calcEntropy(train_data, weight):
    labelCounts = {}
    for i in range(len(train_data)):
        photo_id, orient, pixel = train_data[i]
        if orient not in labelCounts:
            labelCounts[orient] = 0
        labelCounts[orient] += 1.0 * weight[i]
    entropy = 0
    for k in labelCounts:
        prob = labelCounts[k] * 1.0 /len(train_data)
        entropy -= prob * math.log(prob, 2)
    return entropy

def splitDataSet(train_data, pair, value):
    retDataSet = []
    for featVect in train_data:
        photo_id, orient, pixel = featVect
        if decision(pixel, pair[0], pair[1]) == value:
            retDataSet.append(featVect)
    return retDataSet

def chooseBestFeatureToSplit(train_data, weight):
    """
        randomly generate some pairs to try
    """
    bestEntroy = calcEntropy(train_data, weight)
    bestInfoGainRatio = float("-inf")
    bestFeature = (0, 1)

    idx = 0
    while idx < MAXITER:
        pair = tuple(random.sample(VECTOR, 2))
        newEntropy = 0.0
        splitInfo = 0.0

        subDataSet = splitDataSet(train_data, pair, True)
        if len(subDataSet) == 0:
            continue
        prob = len(subDataSet)/float(len(train_data))
        newEntropy += prob * calcEntropy(subDataSet, weight)
        splitInfo += -prob * math.log(prob, 2)

        subDataSet = splitDataSet(train_data, pair, False)
        if len(subDataSet) == 0:
            continue
        prob = len(subDataSet)/float(len(train_data))
        newEntropy += prob * calcEntropy(subDataSet, weight)
        splitInfo += -prob * math.log(prob, 2)

        infoGain = bestEntroy - newEntropy

        if (splitInfo == 0):
            continue
        if (infoGain > bestInfoGainRatio):
            bestInfoGainRatio = infoGain
            bestFeature = pair
        idx += 1

    return bestFeature


def decision_tree(train_data, distrib):
    """
        randomly generate some pairs to try,
        assume first pair seperate 0/90 with 180/270
        second pair separete 0 - 90
        third pair separate 180 -270
    """
    bestFeature = chooseBestFeatureToSplit(train_data, distrib)
    pair1 = bestFeature
    subData1 = splitDataSet(train_data, bestFeature, True)
    subData2 = splitDataSet(train_data, bestFeature, False)

    pair2 = chooseBestFeatureToSplit(subData1, distrib)
    pair3 = chooseBestFeatureToSplit(subData2, distrib)
    
    classifer = Classifer(pair1, pair2, pair3)
    count = {0:0, 1:0, 2:0, 3:0}
    ncount = {0:0, 1:0, 2:0, 3:0}
    for i in range(len(subData1)):
        photo_id, orient, pixel = subData1[i]
        if decision(pixel, pair2[0], pair2[1]):
            count[orient] += 1.0 * distrib[i]
        else:
            ncount[orient] += 1.0 * distrib[i]

    classifer.label1 = max(count, key=count.get)
    classifer.label2 = max(ncount, key=ncount.get)

    count = {0:0, 1:0, 2:0, 3:0}
    ncount = {0:0, 1:0, 2:0, 3:0} 
    for i in range(len(subData2)):
        photo_id, orient, pixel = subData2[i]
        if decision(pixel, pair3[0], pair3[1]):
            count[orient] += 1.0 * distrib[i]
        else:
            ncount[orient] += 1.0 * distrib[i]       
    
    classifer.label3 = max(count, key=count.get)
    classifer.label4 = max(ncount, key=ncount.get)    

    # make sure a valid weeker classifer
    return classifer

 ###########################
 ## adaboost   
def boost(pixel, ensemble):
    count = {0:0, 1:0, 2:0, 3:0}
    for classifer in ensemble:
        label = classifer.predict(pixel)
        count[label] += 1.0 * classifer.weight
    return max(count, key=count.get)

def adaBoostTrain(fname):
    train_data = phaser_txt(fname)
    distrib = [1.0/len(train_data) for i in range(len(train_data))]
    classifer_arr = []
    
    # for t = 1...T
    for i in range(MAX_CLASSIFER):
        # Train weak learner using distribution D
        dec = decision_tree(train_data, distrib)
        # get week hypothesis with error
        error = 0
        for i in range(len(train_data)):
            photo_id, orient, pixel = train_data[i]
            if orient != dec.predict(pixel):
                error += 1.0 * distrib[i]

        # calculate weight
        dec.weight = 0.5 * np.log((1.0-error)/error)
        classifer_arr.append(dec)

        # update distribution
        for i in range(len(train_data)):
            photo_id, orient, pixel = train_data[i]
            if orient == dec.predict(pixel):
                distrib[i] *= np.exp(-dec.weight)
            else:
                distrib[i] *= np.exp(dec.weight)
        total = sum(distrib)
        for i in range(len(distrib)):
            distrib[i] = distrib[i]*1.0/total       
    return classifer_arr

def adaBoostTest(fname, classifer_arr):
    test_data = phaser_txt(fname)
    accurate = 0
    record = []
    for i in range(len(test_data)):
        photo_id, orient, pixel = test_data[i]
        label = boost(pixel, classifer_arr)
        if label == orient:
            accurate += 1
        record.append((photo_id, label))
    print (accurate*1.0/len(test_data))
    display(record, OUTPUT)
    return






