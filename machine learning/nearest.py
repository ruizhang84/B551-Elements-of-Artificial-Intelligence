from shutil import copyfile
from scipy.spatial import distance
import numpy as np
import heapq

OUTPUT = "output.txt"
NEAREST_MODEL = "nearest_model.txt"
K_MEANS = 10

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
            output = photo_id + " " + str(label*90)  + "\n"
            f.write(output)
    return
    
def dist(p1, p2):
    u = np.array(p1)
    v = np.array(p2)
    return distance.euclidean(u, v)


def k_nearest(pixel, train_data, k):
    vote = []
    for i in range(len(train_data)):
        photo_id, orient, pixel2 = train_data[i]
        val = dist(pixel, pixel2)
        heapq.heappush(vote, (val, orient))
    
    # count k neareast voter
    member = {}
    for i in range(k):
        val, orient = heapq.heappop(vote)
        if orient not in member:
            member[orient] = 0
        member[orient] += 1
    return max(member, key=member.get)

def train_nearest(fname, model_file=NEAREST_MODEL):
    copyfile(fname, model_file)
    return

def test_nearest(test_fname, model_fname, k=K_MEANS):
    test_data = phaser_txt(test_fname)
    train_data = phaser_txt(model_fname)
    accurate = 0
    record = []
    for i in range(len(test_data)):
        photo_id, orient, pixel = test_data[i]
        label = k_nearest(pixel, train_data, k)
        if label == orient:
            accurate += 1
            #print accurate
        record.append((photo_id, label))
    print (accurate*1.0/len(test_data))
    display(record, OUTPUT)
    return