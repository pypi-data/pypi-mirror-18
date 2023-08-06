"""
MIT License
"""

import pickle
from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier

# from random import shuffle
# import numpy as np
# import matplotlib.pyplot as plt


class Classifier:
    """ Transportation mode classifier

    This is a wrapper around sklearn SGDClassifier, to simplify it's usage
    """
    def __init__(self):
        self.clf = SGDClassifier(loss="log", penalty="l1", shuffle=False)
        self.labels = preprocessing.LabelEncoder()
        self.learned = False

    def __learn_labels(self, labels):
        """ Learns new labels, this method is intended for internal use
        """
        if self.learned:
            result = list(self.labels.classes_)
        else:
            result = []

        for label in labels:
            result.append(label)
        print(result)
        self.labels.fit(result)

    def learn(self, features, labels):
        """ Fits the classifier

        If it's state is empty, the classifier is fitted, if not
        the classifier is partially fitted.
        See sklearn's SGDClassifier fit and partial_fit methods.

        Args:
            features: Array of arrays with numbers.
            labels: Labels for each set of features. New features are learnt.
        """
        self.__learn_labels(labels)
        labels = self.labels.transform(labels)
        if self.learned:
            self.clf = self.clf.partial_fit(features, labels)
        else:
            print(features, labels)
            self.clf = self.clf.fit(features, labels)
            self.learned = True

    def predict(self, features, verbose=False):
        """ Probability estimates of each feature

        See sklearn's SGDClassifier predict and predict_proba methods.

        Args:
            features: Array of arrays with numbers.
            verbose: Boolean, optional. If true returns an array where each
                element is a dictionary, where keys are labels and values are
                the respective probabilities. Defaults to False.
        Returns:
            Array of array of numbers, or array of dictionaries if verbose i
            True
        """
        probs = self.clf.predict_proba(features)
        if verbose:
            labels = self.labels.classes_
            res = []
            for prob in probs:
                vals = {}
                for i, val in enumerate(prob):
                    label = labels[i]
                    vals[label] = val
                res.append(vals)
            return res
        else:
            return probs

    def save_to_file(self, filename):
        """ Saves this instance to a file

        Args:
            filename: String
        """
        pickle.dump(self, filename)

    @staticmethod
    def load_from_file(filename):
        """ Loads a classifier instance from a file

        Args:
            filename: String
        """
        return pickle.load(filename)

    # def plot(self, colors='rbg', max=10):
    #     result = []
    #     X = np.arange(0, max, 0.1)
    #     for i in X:
    #         [[a, b, c]] = self.predict([[i]])
    #         result.append((a, b, c))
    #     for y in range(3):
    #         plt.plot(X, map(lambda i: i[y], result), '-' + colors[y])


# data = {
#     'stop': [[0], [0.01], [0.05]],
#     'walk': [[0.5], [3], [4], [5]],
#     'car': [[7], [8], [9], [10], [20]]
#     }

# c = Classifier()
#
# data_labels = []
# data_values = []
# items = data.items()
# print(items)
# items = sorted(items, key=lambda i: i[0])
# for label, values in items:
#     for value in values:
#         data_labels.append(label)
#         data_values.append(value)
#
# print(data_labels, data_values)
# c.learn(data_values, data_labels)
# print(c.predict([[10]], verbose=True))
# c.learn([[1]], ['kid'])
# print(c.predict([[10]], verbose=True))
# c.plot(max=30)


# plot_clf(clf)
# plt.show()
