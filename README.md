# iNaturalist Observation Presentation Generator

Generates a presentation showing all a user's observations, organized phylogenetically.

This software is a work-in-progress.

# System Requirements

 - LaTeX (download MacTeX if you are on MacOS)
 - python3
 - python-requests (`pip3 install requests`)

# Quick Start

First, download your observations:

    curl -X GET --header 'Accept: application/json' 'https://api.inaturalist.org/v1/observations?per_page=200&user_id=YOURUSERHERE' > observations.json.raw

I found it useful to format the json:

    json observations.json.raw > observations.json

Then, fetch the associated taxa:

    python fetch-taxa.py

Now, fetch the associated photos:

    python fetch-photos.py

Finally, build the tree and presentation:

    python mk-tree.py


