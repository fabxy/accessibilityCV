import pandas as pd

in_file = "data.csv"
out_base = "accessibility"
out_ext = "txt"

# load data from csv file
df = pd.read_csv(in_file)

# write data to fast.ai format (separate files for each label and no categories)
for l in df.label.unique():
    out_file = '.'.join(['_'.join([out_base, str(l)]), out_ext])
    df[df.label==l].img.to_csv(out_file, index=False, header=False)
    print("%d images with label %d written to %s." % (len(df[df.label==l]), l, out_file))