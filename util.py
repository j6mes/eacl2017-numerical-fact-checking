import re


def normalise(text):
    text = re.sub(r'[^\w]', ' ', text)
    text = re.sub(r'[0-9]','D', text.lower())

    return text

vocab = set()
experiment = 0