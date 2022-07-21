import csv

import requests_cache
from bs4 import BeautifulSoup

session = requests_cache.CachedSession('demo_cache')

all_oblasts_raw = BeautifulSoup(session.get("https://youthcenters.net.ua/perelik-tsentriv-ukraini/").content,
                                "html.parser")

all_oblasts = all_oblasts_raw.find("div", {"class": "centers-list"}).find_all("div",
                                                                              {"class": "centers-list__item row"})

centers_final = []

for oblast in all_oblasts:
    a = oblast.find_all("a")[0]
    link = a["href"]
    oblast_name = a.text
    # print(name)

    url = "https://youthcenters.net.ua" + link
    oblast_centers_raw = session.get(url)
    oblast_centers_cities = BeautifulSoup(oblast_centers_raw.content, "html.parser").find_all("div", {
        "class": "regions-item col"})
    for city in oblast_centers_cities:
        city_name = city.find("a").text
        centers = city.find_all("div", {"class": "regions-list__item row"})
        for center in centers:
            center_name = center.find("a").text
            center_link = "https://youthcenters.net.ua" + center.find("a")["href"]
            print(center_name)
            centers_final.append(
                {"oblast": oblast_name.strip(), "city": city_name.strip(), "center": center_name.strip(),
                 "link": center_link.strip(), })

csv_file = "centers.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["oblast", "city", "center", "link"])

        writer.writeheader()
        for data in centers_final:
            writer.writerow(data)
except IOError:
    print("I/O error")

print("All Done!")
