
def flatten_without_labels(array):
    ret = []
    for key in array:
        if type(array[key]) is not type("") and hasattr(array[key], '__iter__'):
            for item in array[key]:
                ret.append(item)
        else:
            ret.append(array[key])

    return ret


def flatten_with_labels(array):
    ret = []
    for key in array:
        if type(array[key]) is not type("") and hasattr(array[key], '__iter__'):
            for item in array[key]:
                ret.append(key+"$$$"+item)
        else:
            ret.append(key+"$$$"+array[key])

    return ret


if __name__ == "__main__":
    test = {"words":["dog","cat","mouse"],"other_feature":"feature"}

    print(flatten_with_labels(test))
    print(flatten_without_labels(test))