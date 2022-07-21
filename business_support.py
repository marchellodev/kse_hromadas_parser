import csv
import operator

# from datetime import timedeltas
import requests_cache
import json

from bs4 import BeautifulSoup

session = requests_cache.CachedSession('demo_cache')

items = []
page = 1
while True:
    data = session.get('https://business.diia.gov.ua/api/otg/get-items?page='+str(page)+'&per-page=50')
    json_data = json.loads(data.content)

    items.extend(json_data['items'])
    # print(json_data['links']['self'])

    page += 1
    if json_data['links'].get('next') is None:
        break

final_list = []

for el in items:
    details = json.loads(session.get('https://business.diia.gov.ua/api/pages'+el['redirect']).content)

    if details.get('status', 200) != 200:
        continue

    location = details['blocks'][2]['attributes']['properties']
    oblast = ''
    town = ''

    for locationEl in location:
        if 'Область:' in locationEl['label']:
            oblast = str(locationEl['label']).replace('Область: <span>', '').replace('</span>', '')

        if 'Місто:' in locationEl['label']:
            town = str(locationEl['label']).replace('Місто: <span>', '').replace('</span>', '')

    obj = {
        "oblast": oblast,
        "town": town,
        "name": el['label'],
        "category": el['category'],
        "description": el['description'],
        "address": el["address"]["value"],
    }
    final_list.append(obj)

# print(final_list)


csv_file = "business_support.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=final_list[0].keys())

        writer.writeheader()
        for data in final_list:
            writer.writerow(data)
except IOError:
    print("I/O error")
