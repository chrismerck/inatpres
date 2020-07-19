###
###  Input: downloaded observations in observations.json
###
###  curl -X GET --header 'Accept: application/json' 'https://api.inaturalist.org/v1/observations?per_page=200&user_id=chrismerck' > observations.json.raw
###
###  Output:
###
###  directory photo_large/ full of JPG files,
###    organized by subdirs with the taxon id:
###
###    47126/1234567.jpg
###    ...
###

import json
import time
import os
import requests
import shutil

with open('observations.json') as f:
    obs = json.load(f)

for ob in obs['results']:
    taxon_id = None
    try:
        taxon_id = ob['taxon']['ancestor_ids'][-1]
    except:
        print('obs has no taxon?')
        continue
    print(str(taxon_id) + ' --> ', end='')
    dir = 'photo_large/%d'%taxon_id
    if not os.path.exists(dir):
        os.mkdir(dir)
    for index in range(len(ob['observation_photos'])):
        id = ob['observation_photos'][index]['photo']['id']
        fn = '%s/%02d-%s.jpg'%(dir, index, id)
        if os.path.exists(fn):
            print('exists.')
            continue
        r = requests.get('https://static.inaturalist.org/photos/%d/large.jpg'%id, stream=True)
        if r.status_code != 200:
            print('static API error %d' % r.error)
            continue
        with open(fn, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print('DONE!')
        #time.sleep(0.1)

print(obs['total_results'])
print(len(obs['results']))
