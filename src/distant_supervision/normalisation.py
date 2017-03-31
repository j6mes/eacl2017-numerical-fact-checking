import re

def normalise(text):
    text = text.replace("-LRB-","")
    text = text.replace("-LSB-", "")
    text = text.replace("-RRB-", "")
    text = text.replace("-LSB-", "")

    text = re.sub(r'[^\w]', ' ', text)
    text = re.sub(r'[0-9]','D', text.lower())
    return text

def normalisequery(text):
    text = re.sub(r'[^\w]', ' ', text)
    return text.lower()

def normalise_keep_nos(text):
    text = text.replace("-LRB-","")
    text = text.replace("-LSB-", "")
    text = text.replace("-RRB-", "")
    text = text.replace("-LSB-", "")

    text = text.replace(",","")
    text = text.replace(".", "")
    text = text.replace("-", " ")

    text = " ".join(text.lower().strip().split())
    return text