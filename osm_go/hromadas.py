import csv
import operator

# from datetime import timedeltas
import requests_cache
from bs4 import BeautifulSoup
import json

session = requests_cache.CachedSession('demo_cache')

hromada_oblasts_info = BeautifulSoup(session.get("https://gromada.info").content, "html.parser")

# print(hromada_oblasts_info)
oblasts_raw = hromada_oblasts_info.find_all("select")[1].find("optgroup").find_all("option")

resulting_map = []

for oblast in oblasts_raw:
    name_oblast = oblast.text.split(":")[0]
    link = oblast["value"]
    print(name_oblast)
    oblast_info = BeautifulSoup(session.get("https://gromada.info" + link).content, "html.parser")
    oblast_regions_raw = oblast_info.find_all("select")[2].find("optgroup").find_all("option")

    for region in oblast_regions_raw:
        name_region = region.text.split(":")[0]
        link = region["value"]
        print("  "+name_region)
        region_info = BeautifulSoup(session.get("https://gromada.info" + link).content, "html.parser")

        hromadas_raw = region_info.find_all("select")[3].find_all("option")

        for hromada in hromadas_raw:
            name = hromada.text
            link = hromada["value"]
            if name == "Оберіть громаду...":
                continue

            print("    "+name)
            print("    "+link)
            hromada_info = BeautifulSoup(session.get("https://gromada.info" + link).content, "html.parser")
            hromada_map = hromada_info.find_all("script")[8].text.split('var polygon_0 = L.polygon(')[1].split(',{')[0]
            # print(hromada_map)
            resulting_map.append({
                "name": name,
                "region": name_region,
                "oblast": name_oblast,
                "polygon": json.loads(hromada_map)
            })

            # open('test.html', 'w').write(hromada_map.prettify())


            # break


        # break



    # break

json_obj = json.dumps(resulting_map, ensure_ascii=False)
print(len(resulting_map))
open('map.json', 'w').write(json_obj)
