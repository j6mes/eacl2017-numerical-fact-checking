import sys

from table_classifier import train, runtime_predict

if __name__ == "__main__":
    kb=[]
    classifier = train("training",kb)


    while True:
        print("")
        print("")
        q = input("Input statement to check: ")

        print(runtime_predict(q,kb,classifier))