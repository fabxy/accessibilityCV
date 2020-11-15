import webbrowser
import numpy as np
import pandas as pd

# load data
in_file = "data.csv"
df = pd.read_csv(in_file)

# create backup file
df.to_csv(in_file.replace("csv", "bak.csv"), index=False)

# user input
resp = ""

print("Images will show in the browser. Press:")
print("<space> to continue,")
print("<c> to change label,")
print("<d> to delete image,")
# print("<r> to rotate image +90deg,")
# print("<l> to rotate image -90deg,")
print("<q> to quit process.")

while resp != "q":

    # get random image url
    img_idx = np.random.randint(df.shape[0])
    label = df.iloc[img_idx].label
    url_name = df.iloc[img_idx].img
    category = df.iloc[img_idx].category

    # show image in browser
    webbrowser.open(url_name, new=0)

    # get user response
    resp = input("Category %s - Label %d correct?" % (category, label))

    # process response
    if resp == 'd':
        df.drop(img_idx)
        print("Image deleted.")
    elif resp == 'c':        
        new_label = int(not label)
        df.loc[img_idx, 'label'] = new_label
        print("New label is %d" % new_label)

# save modified dataset
df.to_csv(in_file, index=False)
