###
###  Input: downloaded observations in observations.json
###    and  taxa/
###
###  curl -X GET --header 'Accept: application/json' 'https://api.inaturalist.org/v1/observations?per_page=200&user_id=chrismerck' > observations.json.raw
###
###  python fetch-taxa.py
###


import json
import os

with open('observations.json') as f:
    obs = json.load(f)

def new_node():
    return {}

print("#"*30)
print("# Building phylogenetic tree ")
print("#"*30)
tree = {'_name': 'Life', '_rank':'life'}
for ob in obs['results']:
    taxon_id = None
    try:
        taxon_id = ob['taxon']['ancestor_ids'][-1]
    except:
        print('obs has no taxon?')
        continue
    print(str(taxon_id) + ' --> ', end='')
    fn = 'taxa/%d.json'%taxon_id
    if not os.path.exists(fn):
        print('taxon not downloaded yet.')
        continue
    with open(fn) as f:
        taxon = json.load(f)['results'][0]
    print(taxon['name'])
    if 'ancestors' not in taxon:
        print('    ERROR: no ancestors for taxon??')
        continue
    parent = tree
    taxon['ancestors'].append(taxon)
    for a in taxon['ancestors']:
        print('    ' + a['name'] + ': ', end='')
        if a['name'] not in parent:
            print('new')
            node = new_node()
            parent[a['name']] = node
        else:
            node = parent[a['name']]
            print('exists')
        node['_name'] = a['name']
        node['_rank'] = a['rank']
        node['_parent'] = parent
        parent = node

print()
print("# Walking Tree ")

slides = []

def path_str(path):
    return(' -- '.join([node['_name'] for node in path]))

path = None # in media res
def walk(x, indent=0):
    global path
    if len([a for a in x if not a.startswith('_')]) == 0:
        # path slide
        if path is not None:
            path.append(x)
            slides.append({
                'type': 'path',
                'path': path})
        # leaf slide
        slides.append({
            'type': 'taxon',
            'taxon': x})
        path = []
    for a in x:
        if a.startswith('_'):
            continue
        if path is not None: path.append(x)
        walk(x[a], indent+1)
    if path is not None:
        path.append(x)

walk(tree)


## render slides
print()
print("# Rendering Slides...")
print()

def mk_qtree(node, path):
    qtree = ''
    if node in path:
        qtree = r'[.{'
        if path[0] == node or path[-1] == node:
            qtree += r'\strong '
        qtree += r'{\textsc{\tiny %s}} ' % node['_rank']
        qtree += r'%s ' % node['_name']
        qtree += r'\hspace{1cm}'
        qtree += r'} '
    for a in node:
        if a.startswith('_'):
            continue
        qtree += mk_qtree(node[a], path)
    if node in path:
        qtree += ']'
    return qtree


with open('out.tex', 'w') as f:
    f.write(r'''
    \documentclass{beamer}

    \usepackage[utf8]{inputenc}
    \usepackage{qtree}

    \title{iNaturalist Obervations}
    \author{Chris Merck}
    \institute{Overleaf}
    \date{2020}

    \begin{document}

    \frame{\titlepage}
    ''')

    for slide in slides:
        if slide['type'] == 'taxon':
            f.write(r'''
                \begin{frame}
                \frametitle{%s}
                TODO
                \end{frame}
                ''' % (
                    slide['taxon']['_name']
                ))
        elif slide['type'] == 'path':
            qtree = mk_qtree(tree, slide['path'])
            f.write(r'''
                \begin{frame}
                \frametitle{relationship}
                \Tree%s
                \end{frame}
                ''' % (
                    qtree
                ))
            #print(path_str(slide['path']))
            break


    f.write(r'\end{document}')
