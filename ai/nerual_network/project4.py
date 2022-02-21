"""
FILE:        project4.py
AUTHOR:      Miles Wyner, Jack Kaffenbarger
ASSIGNMENT:  Project 4: Neural Networks
DATE:        May 12, 2021

Implements forward and back propogation for neural network learning on some
traning data. Network should be structured to have an input layer corresponding
to the number of inputs in each training case, any number of 1+ sized hidden
layers, and a size 1 output layer for binary classification problems or 2+ for
multi-class or non-classification problems. For example, a network initialized
to
                            nn = NeuralNetwork([2, 3, 1])

would correspond to a binary classification problem and should contain two
inputs for each training case, thus the 2 for the input layer, and nn has 1
hidden layer of size 3, giving the output on the single output node.

Usage: python3 project3.py DATASET.csv
"""

import csv, sys, random, math

def read_data(filename, delimiter=",", has_header=True):
    """Reads datafile using given delimiter. Returns a header and a list of
    the rows of data."""
    data = []
    header = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader, None)
        for line in reader:
            example = [float(x) for x in line]
            data.append(example)

        return header, data

def convert_data_to_pairs(data, header):
    """Turns a data list of lists into a list of (attribute, target) pairs."""
    pairs = []
    for example in data:
        x = []
        y = []
        for i, element in enumerate(example):
            if header[i].startswith("target"):
                y.append(element)
            else:
                x.append(element)
        pair = (x, y)
        pairs.append(pair)
    return pairs

def dot_product(v1, v2):
    """Computes the dot product of v1 and v2"""
    sum = 0
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum

def logistic(x):
    """Logistic / sigmoid function"""
    try:
        denom = (1 + math.e ** -x)
    except OverflowError:
        return 0.0
    return 1.0 / denom

def accuracy(nn, pairs):
    """Computes the accuracy of a network on given pairs. Assumes nn has a
    predict_class method, which gives the predicted class for the last run
    forward_propagate. Also assumes that the y-values only have a single
    element, which is the predicted class.

    Note: this will not work for non-classification problems like the 3-bit
    incrementer."""
    true_positives = 0
    total = len(pairs)

    for (x, y) in pairs:
        nn.forward_propagate(x)

        # CHOOSE ONE
        class_prediction = nn.predict_class()
        # class_prediction = nn.predict_multiclass()

        if class_prediction != y[0]:
            true_positives += 1

    return 1 - (true_positives / total)

def implode(list):
    """Standard impode, helper for crosss validation."""
    answer = []

    for element in list:
        answer.append(element)
    return answer

def normalize_data(filename, delimiter=",", has_header=True):
    """Reads datafile using given delimiter. Returns a header and a list of
    the rows of normalized data."""

    data = []
    header = []
    totals = [0] * 13

    # find means of data
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader, None)

        total_examples = 0

        for line in reader:
            count = 0
            total_examples += 1
            for attribute in line[1:]:
                totals[count] += float(attribute)
                count += 1

        means = [0] * 13
        count = 0
        for attribute in totals:
            means[count] = totals[count] / total_examples
            count += 1

    # find standard deviations of data
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader, None)

        sums_squared = [0] * 13
        stds = [0] * 13

        for line in reader:
            count = 0
            for attribute in line[1:]:
                val = (float(attribute) - means[count])
                sums_squared[count] += val * val
                count += 1

        for i in range(13):
            stds[i] = math.sqrt(sums_squared[i] / (total_examples - 1))

    # find normalized values for data
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader, None)

        for line in reader:
            temp = []
            count = 0
            for data_point in line[1:]:
                temp.append((float(data_point) - means[count]) / stds[count])
                count += 1

            temp.append(float(line[0]))
            data.append(temp)

    return header, data

##############################################################################


class NeuralNetwork:

    def __init__(self, layers):
        """ Initialization of everything the neural network stores. """
        self.layers = layers # list of nodes at each index-->layer number
        self.total_nodes = self.init_total_nodes()
        self.weights = self.init_weights()
        self.activations = [0] * (self.total_nodes + 1)
        self.ALPHA = 0.1

    def init_total_nodes(self):
        """ Find number of total nodes in network. """
        total_nodes = 0
        for nodes in self.layers:
            total_nodes += nodes
        return total_nodes

    def init_weights(self):
        """Initializes grid of None weights. """
        weights = []
        for i in range(self.total_nodes + 1):
            temp_weights = []
            for j in range(self.total_nodes + 1):
                temp_weights.append(None)
            weights.append(temp_weights)
        return weights

    def init_random_weights(self):
        """ Initialization of random weights between nodes and random bias
        weights for all nodes except input nodes. """
        count = 1
        # initialze random weights between nodes
        for layer_nodes in range(len(self.layers) - 1):
            layer_1_nodes = self.layers[layer_nodes]
            layer_2_nodes = self.layers[layer_nodes + 1]
            first_bound = count
            mid_bound = count + layer_1_nodes
            last_bound = count + layer_1_nodes + layer_2_nodes
            count += layer_1_nodes

            for i in range(first_bound, mid_bound):
                for j in range(mid_bound, last_bound):
                    self.weights[i][j] = random.uniform(-1, 1)

        # initialize random node biases
        for i in range(1, self.total_nodes + 1):
            self.weights[0][i] = random.uniform(-1, 1)
        return

    def print_weights(self):
        """Prints weights. """
        for i in self.weights:
            print(i)
        return

    def forward_propagate(self, example):
        """Forward propogate. Takes input of an example, passes it through the
        network and gives some output corresponding to the inputs, using the
        value to update activations array. """

        # input layer activations initialized
        input_count = 0
        for input in example:
            self.activations[input_count] = input
            input_count += 1


        count = 1
        for layer_nodes in range(len(self.layers) - 1):

            # initialize values for loops
            layer_1_nodes = self.layers[layer_nodes]
            layer_2_nodes = self.layers[layer_nodes + 1]
            first_bound = count
            mid_bound = count + layer_1_nodes
            last_bound = count + layer_1_nodes + layer_2_nodes
            count += layer_1_nodes

            # find activation going into node j from all connected node i's
            for j in range(mid_bound, last_bound):
                activation = 0
                for i in range(first_bound, mid_bound):
                    activation += (self.weights[i][j] * self.activations[i])

                # update activation value found by logistic function
                self.activations[j] = logistic(activation + self.weights[0][j])

        return

    def back_propagation_learning(self, ex):
        """Back propogate. Takes the output of some example, passes it back
        through the network to update weights in order to give better outputs,
        finding error between nn output of forward propogation and example
        output first, using the error to inform slight changes to weights in
        the network. """

        error_changes = [0] * (self.total_nodes + 1)

        # find errors for output layer
        for i in range(self.total_nodes - self.layers[-1] + 1, self.total_nodes + 1):
            error_changes[i] = self.activations[i] * \
                               (1 - self.activations[i]) * \
                               (ex[0] - self.activations[i])

        # find errors for other layers
        count = self.total_nodes
        upper_bound = len(self.layers) - 1

        while upper_bound > 1:

            # bounds values for layers
            outer_nodes = self.layers[upper_bound]
            inner_nodes = self.layers[upper_bound - 1]
            last_bound = count + 1
            mid_bound = count - outer_nodes + 1
            first_bound = count - outer_nodes - inner_nodes + 1
            count -= outer_nodes
            upper_bound -= 1

            for i in range(first_bound, mid_bound):
                sum = 0
                for j in range(mid_bound, last_bound):
                    sum += self.weights[i][j] * error_changes[j]
                error_changes[i] += self.activations[i] * (1 - self.activations[i]) * sum

        # tweak weights
        count = 1
        for layer_nodes in range(len(self.layers) - 1):

            # bounds values for layers
            layer_1_nodes = self.layers[layer_nodes]
            layer_2_nodes = self.layers[layer_nodes + 1]
            first_bound = count
            mid_bound = count + layer_1_nodes
            last_bound = count + layer_1_nodes + layer_2_nodes
            count += layer_1_nodes

            for i in range(first_bound, mid_bound):
                for j in range(mid_bound, last_bound):
                    self.weights[i][j] += self.ALPHA * self.activations[i] * error_changes[j]

        # tweak bias values for all nodes except input layer nodes
        for i in range(self.layers[0] + 1, self.total_nodes + 1):
            self.weights[0][i] += self.ALPHA * self.activations[0] * error_changes[i]

        return

    def predict_class(self):
        """ Gives the predicted class for binary classification problems. """
        if self.activations[self.total_nodes] >= 0.5:
            return 1.0
        return 0.0

    def predict_multiclass(self):
        """ Gives the predicted class for multi-class classification problems."""

        max = 0, 0
        count = 0

        # Finds greatest probability value in list of outputs, returns index + 1
        for i in range(self.total_nodes - self.layers[-1] + 1, self.total_nodes + 1):
            # print(self.activations[i])
            if self.activations[i] > max[0]:
                max = self.activations[i], count
            count += 1

        return max[1] + 1

    def kfold_cross_validation(self, pairs, k):
        """ Utilizes cross validation of data to test applicability of network
        on unseen data. """

        k_lists = []
        increment = len(pairs) // k

        # initialize list of k lists, each containing n // k of the examples
        for i in range(k):
            new_list = pairs[increment * i:increment * (i + 1)]
            k_lists.append(new_list)

        total_accuracy = 0

        # split examples into
        #       a. learning cases (list of size n - n / k)
        #       b. test cases (list of size n / k)
        for i in range(k):
            learning_cases = implode(k_lists[:i] + k_lists[i + 1:])[0]
            learning_cases = [([1.0] + x, y) for (x, y) in learning_cases]
            test_cases = k_lists[i]
            self.init_random_weights()


            # run learning on current learning cases
            epochs = 500

            while epochs != 0:
                for case in learning_cases:
                    # self.print_weights()
                    self.forward_propagate(case[0])
                    self.back_propagation_learning(case[1])
                    # self.print_weights()
                accuracy_check = accuracy(self, pairs)
                print("Epoch {} has accuracy {}".format(500 - epochs, accuracy_check))
                epochs -= 1


            # find accuracy on current test cases (excluded from learning)
            print(accuracy(self, test_cases))
            total_accuracy += accuracy(self, test_cases)

        # find average accuracy over all k iterations
        average_accuracy = total_accuracy / k
        return average_accuracy


def main():

    ##########################################################################
    # Choose method to read files

    # for binary, non- classification
    # ***IF CHOSEN, must change accuracy function to predict_class
    header, data = read_data(sys.argv[1], ",")

    # for multi-class classification (wine.csv)
    # ***IF CHOSEN, must change accuracy function to predict_multiclass
    # header, data = normalize_data(sys.argv[1], ",")

    ##########################################################################
    # Convert data to more useable type, add dummy values

    pairs = convert_data_to_pairs(data, header)
    # Note: add 1.0 to the front of each x vector to account for the dummy input
    training = [([1.0] + x, y) for (x, y) in pairs]

    ##########################################################################
    # initialization of network and learning

    nn = NeuralNetwork([2, 3, 1])
    nn.init_random_weights()

    # learning algorithm
    epochs = 2000
    while epochs != 0:
        for example in training:
            nn.forward_propagate(example[0])
            nn.back_propagation_learning(example[1])
        accuracy_check = accuracy(nn, pairs)
        print("Epoch {} has accuracy {}".format(2000 - epochs, accuracy_check))
        epochs -= 1

    # works for binary and multi-class classification
    accuracy_check = accuracy(nn, pairs)
    print(accuracy_check)

    ##########################################################################
    # Cross validation

    # nn = NeuralNetwork([2, 3, 1])
    # nn.init_random_weights()
    # accuracy = nn.kfold_cross_validation(pairs, 3)
    # print(accuracy)

    ##########################################################################
    # Increment-3-bit test
    # Must go into predict multiclass and backward propoagate to correctly
    # get the right output
    
    # for (x, y) in pairs:
    #     answer = []
    #     nn.forward_propagate(x)
    #     for output in nn.activations[10:]:
    #         answer.append(round(output))
    #     print("x: ", x, "y: ", y, "our y: ", answer)

    ##########################################################################
    # Hard coded class example

    # nn = NeuralNetwork([2, 2, 1])
    # nn.weights[0][3] = 0.5
    # nn.weights[0][4] = -1
    # nn.weights[0][5] = -1
    # nn.weights[1][3] = 3
    # nn.weights[1][4] = -2
    # nn.weights[2][3] = -2
    # nn.weights[2][4] = 4
    # nn.weights[4][5] = 2
    # nn.weights[3][5] = 0.5
    #
    # training = [[1, 3, 4], [1]]
    # nn.forward_propagate(training[0])
    # nn.back_propagation_learning(training[1])

    ##########################################################################
    # testing

    # accuracy_list = []
    #
    # for i in range (1, 10):
    #     nn = NeuralNetwork([2, i, 1])
    #     nn.init_random_weights()
    #     accuracy = nn.kfold_cross_validation(pairs, 5)
    #     accuracy_list.append((i, accuracy))
    # print(accuracy_list)



if __name__ == "__main__":
    main()
