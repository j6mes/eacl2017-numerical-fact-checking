from tabular.filter_collection import read_filters_collection
from tabular.filtering import load_collection, write_collection

country_filters = read_filters_collection("countries")
tables = load_collection("training")
#tables.append_collection("pristine-seen-tables")
#tables.append_collection("pristine-seen-tables")

out_tables = set()

for filter in country_filters:
    t = tables.get_tables_for_word(filter)
    out_tables.update(t['exact'])
    out_tables.update(t['partial'])


write_collection("countries",out_tables)

