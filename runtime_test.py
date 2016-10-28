from table_classifier import train, runtime_predict

if __name__ == "__main__":
    kb=[]
    classifier = train("training",kb)

    while True:
        q = input("Enter Question")
        runtime_predict(q,kb,classifier)