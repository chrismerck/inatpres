###
###  Input: downloaded observations in observations.json
###
###  curl -X GET --header 'Accept: application/json' 'https://api.inaturalist.org/v1/observations?per_page=200&user_id=chrismerck' > observations.json.raw
###
###  Output:
###
###  directory taxa/ full of json files:
###
###    47126.json
###    ...
###

import json
import time
import os
import requests

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
    fn = 'taxa/%d.json'%taxon_id
    if os.path.exists(fn):
        print('exists.')
        continue
    r = requests.get('https://api.inaturalist.org/v1/taxa/%d'%taxon_id)
    if r.status_code != 200:
        print('taxa API error %d' % r.error)
        continue
    with open('taxa/%d.json'%taxon_id, 'w') as f:
        f.write(r.text)
    print('DONE!')
    time.sleep(1)

print(obs['total_results'])
print(len(obs['results']))
