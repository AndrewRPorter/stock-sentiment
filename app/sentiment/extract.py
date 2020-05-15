"""
By default, the NaiveBayesClassifier uses a simple feature extractor that indicates which words in the training set are contained in a document.

For example, the sentence “I feel happy” might have the features contains(happy): True or contains(angry): False.

You can override this feature extractor by writing your own. A feature extractor is simply a function with document (the text to extract features from) as the first argument. The function may include a second argument, train_set (the training dataset), if necessary.

The function should return a dictionary of features for document.

For example, let’s create a feature extractor that just uses the first and last words of a document as its features.

>>> def end_word_extractor(document):
...     tokens = document.split()
...     first_word, last_word = tokens[0], tokens[-1]
...     feats = {}
...     feats["first({0})".format(first_word)] = True
...     feats["last({0})".format(last_word)] = False
...     return feats
>>> features = end_word_extractor("I feel happy")
>>> assert features == {'last(happy)': False, 'first(I)': True}

We can then use the feature extractor in a classifier by passing it as the second argument of the constructor.

>>> cl2 = NaiveBayesClassifier(test, feature_extractor=end_word_extractor)
>>> blob = TextBlob("I'm excited to try my new classifier.", classifier=cl2)
>>> blob.classify()
'pos'
"""


def custom_feature_extractor(text):
    pass
