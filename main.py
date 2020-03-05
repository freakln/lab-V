import csv

import requests

query_type = ['search', 'user', 'organization', 'repository']
search_type = ['search', 'user', 'organization', 'repository']
length = 0
after = ' '

query = 'query{search(query:"stars:>100", type:REPOSITORY, first:100' + after + '){' \
                                                                                'pageInfo{hasNextPage endCursor}' \
                                                                                'nodes{... ' \
                                                                                'on Repository{' \
                                                                                'nameWithOwner url createdAt}}}}'
dado = ''
print(query)
have_next_page = True
page = 1
nodes = list()
while have_next_page and page < 10:
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    print(request.status_code)

    if request.status_code == 200:
        result = request.json()

        nodes += result['data']['search']['nodes']

        have_next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
        page += 1
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        after = ", after:{}".format(cursor)
    print(nodes)

names = []
to_csv = []

for d in nodes:
    row = {}
    for keys in d.keys():
        if keys not in names:
            names.append(keys)
        row.update({keys: d[keys]})
    to_csv.append(row)

with open('resultados.csv', mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=names, delimiter=';')
    writer.writeheader()
    for i in to_csv:
        writer.writerow(i)
