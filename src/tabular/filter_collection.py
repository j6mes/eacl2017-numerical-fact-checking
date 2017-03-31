def read_filters_collection(filters_file,base="data/filtering/"):
    parts = []
    with open(base+filters_file+".txt","r") as f:
        for line in f:
            parts.extend(line.strip().split("|"))

    return parts


if __name__=="__main__":
    read_filters_collection("countries")