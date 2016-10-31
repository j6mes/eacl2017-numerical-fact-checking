import sys

from table_classifier import train, runtime_predict

if __name__ == "__main__":
    kb=[]
    classifier = train("pristine-unseen-tables",kb)


    while True:
        q = input("Enter Question\n")
        runtime_predict(q,kb,classifier)