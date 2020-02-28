import csv

import requests

query_type = ['search', 'user', 'organization', 'repository']
search_type = ['search', 'user', 'organization', 'repository']
length = 0


quersy = 'query example {search(query:"stars:>100",type:REPOSITORY, first:100){nodes {... on Repository {nameWithOwner ' \
         'diskUsage}}}} '
print(quersy)


def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        print(request.json())
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


names = []
to_csv = []
dados = run_query(quersy)
print(dados['data']['search']['nodes'])
for d in dados['data']['search']['nodes']:
    row = {}
    for keys in d.keys():
        if keys not in names:
            names.append(keys)
        row.update({keys: d[keys]})
    to_csv.append(row)

with open('amis.csv', mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=names, delimiter=';')
    writer.writeheader()
    for i in to_csv:
        writer.writerow(i)
