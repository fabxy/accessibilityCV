import json
import pandas as pd

# load raw data
in_file = "raw_data.json"

f = open(in_file, 'r')
raw_data = json.load(f)
f.close()

# loop over data
data = []
no_label = 0

for key in raw_data.keys():

    try:
        label = int(raw_data[key]['info']['accessibility']['accessibleWith']['wheelchair'])
    except:
        no_label += 1
        print('Accessibility label for key %s missing (count: %d).' % (key, no_label))
        continue

    try:
        for img in raw_data[key]["photos"]:
            data.append([img['original'], label])
    except:
        no_label += 1
        print('Image label for key %s missing (count: %d).' % (key, no_label))
        continue

# convert to DataFrame and write csv
out_file = "data.csv"
df = pd.DataFrame(data, columns=['img','label'])
df.to_csv(out_file)