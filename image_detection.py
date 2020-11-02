import requests
import json
import re
import os
from tqdm import tqdm

# identify matching bracket
def find_bracket(in_str, start_idx):

    count = 1
    idx = start_idx

    while count > 0:
        
        if in_str[idx] == '[':
            count += 1
        elif in_str[idx] == ']':
            count -= 1
        idx += 1

    return idx-1

# load API data
in_file = "api_data.json"
f = open(in_file, 'r')
data = json.load(f)
f.close()

# read existing log file
log_file = "log.csv"
log_dict = {}

if log_file in os.listdir():

    # read log file
    f = open(log_file, 'r')
    
    for line in f:
        
        line = line[:-1]
        key = '/'.join(line.split(',')[1:4])
        
        # add new key
        if key not in log_dict.keys():
            log_dict[key] = []
        
        # add object with image index
        try:
            log_dict[key].append(int(line.split(',')[4]))
        except:
            pass

    f.close()

# loop over tiles
res = {}
img_count = 0
tile_num = len(data.keys())

for i, key in enumerate(data.keys()):

    # set tile title
    tqdm_desc = "Tile %d/%d" % (i+1, tile_num)

    # check if tile available in log
    if key in log_dict.keys():
        pbar = tqdm(log_dict[key], desc=tqdm_desc)
    else:
        pbar = tqdm(range(data[key]['featureCount']), desc=tqdm_desc)

    # loop over objects in tile
    for obj in pbar:

        # check page URL information
        try:
            info_url = data[key]['features'][obj]['properties']['infoPageUrl']
            if 'wheelmap' in info_url:
                pass
            else:
                continue
        except:
            continue

        # access wheelmap.org node
        r = requests.get(info_url)

        # request successful
        if r.status_code == 200:
        
            # identify photo section
            ms = [m.end() for m in re.finditer('"photos":\[', r.text)]

            if len(ms) == 1:
                
                # photo section indices
                start_idx = ms[0] - 1
                end_idx = find_bracket(r.text, ms[0])

                # interpret pattern as json
                photo_str = r.text[start_idx:end_idx+1]
                d = json.loads(photo_str)

                # check if object has image and add to results
                if len(d) > 0:

                    id = data[key]['features'][obj]['properties']['_id']

                    res[id] = {
                        'info': data[key]['features'][obj]['properties'],
                        'photos': d,
                    }

                    img_count += 1

                    # save objects with images
                    if key not in log_dict.keys():
                        f = open(log_file, 'a+')
                        f.write("%d,%s,%d\n" % (img_count, key.replace('/',','), obj))
                        f.close()

            elif len(ms) > 1:
                raise RuntimeError("ERROR: Unexpected pattern for object %d in tile %s!" % (obj, key))
                            
        # unsuccessful request
        else:
            print("WARNING: Request to %s unsuccessful." % info_url)

        # modify processbar
        pbar.set_postfix_str(s="Image objects: %d" % img_count)

    # save completely searched keys
    if key not in log_dict.keys():
        f = open(log_file, 'a+')
        f.write("%d,%s\n" % (img_count, key.replace('/',',')))
        f.close()

# save results
res_file = "raw_data.json"
f = open(res_file, 'w')
json.dump(res, f)
f.close()