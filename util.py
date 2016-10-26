import re


def normalise(text):
    text = re.sub(r'[^\w]', ' ', text)
    text = re.sub(r'[0-9]','D', text.lower())

    return text

vocab = set()
vocab_ngrams = set()

experiment_bow = 0
experiment_ngrams = 0