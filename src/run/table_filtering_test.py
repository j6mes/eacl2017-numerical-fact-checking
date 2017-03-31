
from tabular.filtering import load_collection
from tabular.tuples import get_all_tuples

if __name__ == "__main__":
    tables = load_collection("training")
    print(get_all_tuples(tables,"Japan"))