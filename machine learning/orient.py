from nearest import *
from nnet import *
from adaboost import *
import sys, time

OUTPUT = "output.txt"
NEAREST_MODEL = "nearest_model.txt"
ADABOOST_MODEL = "adaboost_model.txt"
NN_MODEL = "nnet_model.txt"

# ./orient.py train/test train_file.txt/test_file model_file.txt [model]
program, train_test, input_data, model_file, model = sys.argv
if model == "nearest":
    # train model
    if train_test == "train":
        train_nearest(input_data, model_file)
    # test model
    elif train_test == "test":
        start = time.time()
        test_nearest(input_data, model_file, 10)
        elapsed = time.time() - start
        print (elapsed)

elif model == "adaboost":
    if train_test == "train":
        start = time.time()
        classifer_arr = adaBoostTrain(input_data)
        adaBoostModel(model_file, classifer_arr)
        elapsed = time.time() - start
        print (elapsed)
    elif train_test == "test":
        classifer_arr = loadAdaBoostModel(model_file)
        adaBoostTest(input_data, classifer_arr)

elif model == "nnet":
    if train_test == "train":
        start = time.time()
        train_nnet(input_data, 0.1, [10, 10, 4], 20000, model_file)
        elapsed = time.time() - start
        print (elapsed)
    elif train_test == "test":
        test_nnet(input_data, model_file)

elif model == "best":
    if train_test == "train":
        train_nnet(input_data, 0.1, [10, 10, 10, 4], 200000, model_file)
    elif train_test == "test":
        test_nnet(input_data, model_file)  


