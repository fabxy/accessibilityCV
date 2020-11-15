import json
import pandas as pd

# options
in_file = "raw_data.json"
out_file = "data.csv"
incl_part = 0
show_cats = 0
excl_cats = [
    "undefined",
    "public_art",
    "atm",
    "memorial",
    "toilets",
    "bus_stop",
    "company",
    "train_station",
    "soccer",
    "attraction",
    "arts_center",
    "nightclub",
    "car_repair",
    "biergarten",
    "hiking",
    "subway_station",
    "diy",
    "instruments",
    "drinkingwater",
    "tram_stop",
    "cinema",
    "parking",
    "public_transport",    
]

# load raw data
f = open(in_file, 'r')
raw_data = json.load(f)
f.close()

# loop over data
data = []
cats = {}
no_label = 0
part_count = 0

for key in raw_data.keys():

    # get category
    try:
        cat = raw_data[key]['info']['category']
        if cat in cats.keys():
            cats[cat] += 1
        else:
            cats[cat] = 1
    except:
        print('Category for key %s missing.' % (key))
        cat = None

    # get label
    try:
        label = int(raw_data[key]['info']['accessibility']['accessibleWith']['wheelchair'])

        # check partial accessibility    
        if label == 0:
            try: 
                if raw_data[key]['info']['accessibility']['partiallyAccessibleWith']['wheelchair']:
                    if incl_part:
                        label = 2
                        part_count += 1
                    else:
                        continue
            except:
                pass
    except:
        no_label += 1
        print('Accessibility label for key %s missing (count: %d).' % (key, no_label))
        continue

    # get image url
    try:
        for img in raw_data[key]["photos"]:
            data.append([img['original'], label, cat])
    except:
        no_label += 1
        print('Image label for key %s missing (count: %d).' % (key, no_label))
        continue

# show object categories
if show_cats:
    print("Following categories are present in data:")
    for cat in sorted(cats.keys(), key=lambda x: cats[x], reverse=True):
        print("%s: %s" % (str(cats[cat]).zfill(4), cat))

# print info on partial accessibility
if incl_part:
    print("%d partially accessible objects in data." % part_count)

# convert to DataFrame and write csv
if out_file is not None:
    df = pd.DataFrame(data, columns=['img','label','category'])

    # exclude specified categories
    cat_filter = (df.category.isnull() | df.category.isin(excl_cats))
    
    df[~cat_filter].to_csv(out_file, index=False)
    print("%d images written to %s." % (len(data), out_file))