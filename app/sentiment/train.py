import os
import pickle

from textblob import classifiers, exceptions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_FILE = "sentiment/data/train.json"

CLASSIFY_FILE = "sentiment/classifier.pickle"

classifier = None  # global classification object


def retrain():
    """
    Re-trains the Naive Bayes classifier
    https://textblob.readthedocs.io/en/dev/classifiers.html
    """

    FILE_PATH = os.path.join(BASE_DIR, TRAIN_FILE)

    with open(FILE_PATH, "r") as fp:
        try:
            cl = classifiers.NaiveBayesClassifier(fp, format="json")
        except exceptions.MissingCorpusError:
            return None

    return cl


def serialize(file_name):
    """Dumps classifier serialized data after re-training"""
    cl = retrain()

    with open(file_name, "wb") as f:
        pickle.dump(cl, f)


def get_classifier():
    """Returns the un-serialized pickled classifier"""
    global classifier
    FILE_NAME = os.path.join(BASE_DIR, CLASSIFY_FILE)

    if not os.path.isfile(FILE_NAME):
        serialize(FILE_NAME)

    if classifier == None:  # check to see if classifier needs to be re-initialized
        with open(FILE_NAME, "rb") as f:
            if os.path.getsize(FILE_NAME) > 0:
                classifier = pickle.load(f)

    return classifier


def setup():
    """Checks to see if serialized data exists at runtime"""
    global classifier
    FILE_NAME = os.path.join(BASE_DIR, CLASSIFY_FILE)

    if not os.path.isfile(FILE_NAME):
        serialize(FILE_NAME)

    # set the global classifier variable
    with open(FILE_NAME, "rb") as f:
        if os.path.getsize(FILE_NAME) > 0:
            classifier = pickle.load(f)


if __name__ == "__main__":
    setup()
