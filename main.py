import csv
import time
import requests

inicio = time.time()
names = []
to_csv = []

query_type = ['search', 'user', 'organization', 'repository']
search_type = ['search', 'user', 'organization', 'repository']
length = 0
after = ''
headers = {"Authorization": "token 646bf7fcbcfe9f865a54d608aa50c1da151eb98b"}
query = 'query{search(query:"stars:>100", type:REPOSITORY, first:10 %s ){' \
        'pageInfo{hasNextPage endCursor}' \
        'nodes{... ' \
        'on Repository{' \
        'nameWithOwner primaryLanguage{name} createdAt pullRequests(states:MERGED){totalCount}' \
        ' updatedAt releases {totalCount} opened_issues: issues{totalCount} closed_issues: issues(states:CLOSED){totalCount}}}}}'

dado = ''
cursor = ''
have_next_page = True
page = 0

mquery = query % after
print(mquery)
nodes = list()
while have_next_page and page < 100:

    request = requests.post('https://api.github.com/graphql', json={'query': mquery}, headers=headers)
    print('page:' + str(page))
    print(request.status_code)
    if request.status_code == 200:
        result = request.json()

        nodes += result['data']['search']['nodes']

        have_next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
        page += 1
        print(result["data"]["search"]["pageInfo"]["endCursor"])
        after = ', after:"' + result["data"]["search"]["pageInfo"]["endCursor"]+'"'
        mquery = query % after


for d in nodes:
    row = {}
    for keys in d.keys():
        if keys not in names:
            names.append(keys)
        row.update({keys: d[keys]})
    to_csv.append(row)

with open('resultado_2.csv', mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=names, delimiter=';')
    writer.writeheader()
    for i in to_csv:
        writer.writerow(i)

print(time.time() - inicio)
