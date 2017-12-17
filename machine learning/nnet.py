import numpy as np
IINIT_EPSILON = 1
MODEL_FILE = "nnet_model.txt"
OUTPUT = "output.txt"

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

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

class NeuralNetwork:
    def __init__(self, alpha, layer_sizes, max_iter=20000, weight=[], random_state=0):
        """
            alpha: learning rate
            max_iter: maximum iterations
            tol: tolerance
            layer_sizes: ith element represents the number of neurons in the ith layer,
                         including input + hidden layer + output,
                         if ntework has s_j units in layer j,
                         s_{j+1} units in layer j+1, then weight be of s_{j+1}x(s_j+1).
        """
        np.random.seed(random_state)
        self.alpha = alpha
        self.max_iter = max_iter
        self.layers = layer_sizes

        self.weight = weight
        if len(self.weight) == 0:
            for i in range(len(layer_sizes)-1):
                self.weight.append(
                    np.random.random((layer_sizes[i] + 1, layer_sizes[i+1]))
                    * (2 * IINIT_EPSILON) - IINIT_EPSILON)
        
    def fit(self, X, y):
        """
            X: array X of size (n_samples, n_features)
            Y: array y of size (n_samples)
        """
        y = np.atleast_2d(y)

        for i in range(self.max_iter):
            # Feed forward
            a = []
            # adding bais units
            temp = np.hstack((np.ones((X.shape[0], 1)), X))
            a.append(temp)
            for j in range(len(self.weight)):
                # sigmoid h(theta)
                z = np.dot(temp, self.weight[j])
                temp = sigmoid(z)
                # adding bais units
                if j != len(self.weight) -1:
                    temp = np.hstack((np.ones((temp.shape[0], 1)), temp))
                a.append(temp)    
        
            # output layer error term
            error = y - a[-1]
            deltas = [error]

            # backprobagation
            for k in range(len(a)-2, 0, -1):
                error = np.dot(error, self.weight[k].T) * a[k] * (1 - a[k])
                error = error[:,1:]
                deltas.append(error)
            deltas.reverse()
        
            for k in range(len(self.weight)):
                delta = a[k][:, :, np.newaxis] * deltas[k][: , np.newaxis, :]
                ave_delta = np.average(delta, axis=0)
                self.weight[k] += self.alpha * ave_delta

    def predict(self, X):
        a = np.atleast_2d(X)
        for i in range(len(self.weight)):
            a = np.hstack((np.ones((a.shape[0], 1)), a))
            a = np.dot(a, self.weight[i])
            a = sigmoid(a)
        return a

def Standardize(X, mean, std):
    return (X - mean)/std

def pca_fit(X, dim):
    x_T = np.transpose(X)
    x_cov = (np.cov(x_T))
    eigVals, eigVects=np.linalg.eigh(x_cov)

    idx = np.argsort(-eigVals)
    eigVects = eigVects.T[:,idx]
    eigVals = eigVals[idx]
    eigVects = eigVects[:, :dim]

    X = np.dot(eigVects.T, X.T).T
    return (X, eigVects)

def pca_transform(X, eigVects):
    X = np.dot(eigVects.T, X.T).T
    return X

def process_data(train_data, dimensions=10):
    X = []
    y = []
    for i in range(len(train_data)):
        photo_id, orient, pixel= train_data[i]
        X.append(pixel)
        y.append(orient)

    # Standardize features by removing the mean and scaling to unit variance
    # x = (x-mean)/std
    X = np.array(X)
    mean = np.mean(X)
    std = np.std(X)
    X = Standardize(X, mean, std)   

    # PCA to decrease dimensions
    X, vec = pca_fit(X, dimensions)

    # convert y to vector
    for i in range(len(y)):
        temp = [0, 0, 0, 0]
        temp[y[i]] = 1
        y[i] = temp
    return (X, y, mean, std, vec)

def train_nn(X, y, alpha, layer, max_iter):
    nn = NeuralNetwork(alpha, layer, max_iter)
    nn.fit(X, y)
    return nn

def argmax(arr):
    idx = 0
    max_v = arr[0]
    for i in range(len(arr)):
        if max_v < arr[i]:
            idx = i
            max_v = arr[i]
    return idx

def test_nn(nn, test_data, mean, std, vec):
    def convert_label(y):
        labels = []
        for n in y:
            labels.append(argmax(n))
        return labels
    X = []
    for i in range(len(test_data)):
        photo_id, orient, pixel= test_data[i]
        X.append(pixel)
    X = np.array(X)
    X = Standardize(X, mean, std)
    X = pca_transform(X, vec)
    labels = convert_label(nn.predict(X))

    # accuracy
    accurate = 0
    record = []
    for i in range(len(test_data)):
        photo_id, orient, pixel= test_data[i]
        if labels[i] == orient:
            accurate += 1
        record.append((photo_id, labels[i]))
    print (accurate*1.0/len(test_data))
    display(record, OUTPUT)
    return

def nn_model(fname, nn, mean, std, vec):
    with open(fname, 'w') as f:
        f.write(str(nn.max_iter) + "\n")
        f.write(str(nn.alpha) + "\n")
        f.write(str(mean) + "\n")
        f.write(str(std) + "\n")
        temp = [str(i) for i in vec]

        n = len(vec)
        f.write(str(n) + "\n")
        for i in range(n):
            temp = [str(j) for j in vec[i]]
            f.write(" ".join(temp) + "\n")

        temp = [str(i) for i in nn.layers]
        f.write(" ".join(temp) + "\n")

        n = len(nn.weight)
        f.write(str(n) + "\n")

        for i in range(n):
            m = len(nn.weight[i])
            f.write(str(m) + "\n")
            for j in range(m):
                temp = [str(x) for x in nn.weight[i][j]]
                f.write(" ".join(temp) + "\n")
    return

def nn_loadModel(fname):
    with open(fname, 'r') as f:
        iters = int(f.readline().strip())
        alpha = float(f.readline().strip())
        mean = float(f.readline().strip())
        std = float(f.readline().strip())
        n = int(f.readline().strip())
        vec = []
        for i in range(n):
            line = f.readline().strip().split(" ")
            temp = [float(i) for i in line]
            temp = np.array(temp)
            vec.append(temp)
        vec = np.array(vec)
        
        line = f.readline().strip().split(" ")
        layer_size = [int(i) for i in line]

        n = f.readline().strip()
        n = int(n)
        weight = []
        for i in range(n):
            m = f.readline().strip()
            m = int(m)
            temp = []
            for j in range(m):
                line = f.readline().strip().split(" ")
                temp.append([float(x) for x in line])
            temp = np.array(temp)
            weight.append(temp) 
        nn = NeuralNetwork(alpha, layer_size, iters, weight)
    return (nn, mean, std, vec)

def train_nnet(fname, alpha, layer_sizes, iters, model_file=MODEL_FILE):
    train_data = phaser_txt(fname)
    X, y, mean, std, vec = process_data(train_data, layer_sizes[0])
    nn = train_nn(X, y, alpha, layer_sizes, iters)
    nn_model(model_file, nn, mean, std, vec)

def test_nnet(fname, model_file):
    test_data = phaser_txt(fname)
    nn, mean, std, vect = nn_loadModel(model_file)
    test_nn(nn, test_data, mean, std, vect)

