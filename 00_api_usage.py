"""Learning how to access an API using Python."""

import numpy as np
import requests
import json

# convert lat/lon/zoom to x/y
def convert_to_xy(lat, lon, zoom):

    lat_rad = np.radians(lat)
    n = 2.0 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - np.arcsinh(np.tan(lat_rad)) / np.pi) / 2.0 * n)

    return x, y


# website address
url = "https://accessibility-cloud.freetls.fastly.net/place-infos.json"

# load API key
f = open("./.apptoken", 'r')
api_key = f.read()
api_key = api_key.replace("\n", "")
f.close()

# determine scraping area in x/y/zoom coordinates (https://developers.planet.com/tutorials/slippy-maps-101/)
# view tiles via "https://a.tile.openstreetmap.org/<ZOOM>/<X>/<Y>.png"
# NOTE: zoom needs to be adapted such that totalFeatureCount is smaller than 1000

w_lat = 52.5007919
w_lon = 13.2839193

s_lat = 52.4759806
s_lon = 13.3650726

o_lat = 52.5028779
o_lon = 13.4696738

n_lat = 52.5491748
n_lon = 13.3900758

zoom = 15

x_min, _ = convert_to_xy(w_lat, w_lon, zoom)
_, y_min = convert_to_xy(n_lat, n_lon, zoom)
x_max, _ = convert_to_xy(o_lat, o_lon, zoom)
_, y_max = convert_to_xy(s_lat, s_lon, zoom)

x_coords = np.arange(x_min, x_max)
y_coords = np.arange(y_min, y_max)

# loop over coordinates
data = {}
obj_num = 0

print("Number of requests: %d" % (len(x_coords) * len(y_coords)))

for x in x_coords:
    for y in y_coords:

        # request parameters
        params = {
            "appToken": api_key,
            "x": x,
            "y": y,
            "z": zoom,
        }

        # make API request
        r = requests.get(url=url, params=params)

        # successful request
        if r.status_code == 200:
            r_data = r.json()

            # check if all objects were scraped
            if r_data['featureCount'] != r_data['totalFeatureCount']:
                raise RuntimeWarning("WARNING: Not all objects included. Increase zoom level!")
            
            # add scraped data to dict
            dict_key = '%d/%d/%d' % (zoom, x, y)
            data[dict_key] = r_data
            
            # count number of scrapped objects
            obj_num += r_data['featureCount']

            print("Request for tile %s successful." % dict_key)

        # unsuccessful request
        else:
            raise RuntimeWarning("WARNING: Request for tile %d/%d/%d failed!" % (zoom, x, y))
       
# report number of scrapped objects
print("Objects found: %d" % obj_num)

# save data
out_file = "api_data.json"
f = open(out_file, 'w')
json.dump(data, f)
f.close()