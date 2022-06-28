import csv
import operator

# from datetime import timedeltas
import requests_cache
from bs4 import BeautifulSoup

session = requests_cache.CachedSession('demo_cache')

all_oblasts_raw = BeautifulSoup(session.get("https://decentralization.gov.ua/areas").content, "html.parser")
oblast_rows = all_oblasts_raw.find(id="areas-list").find_all("div", class_="row")

oblasts = []

for oblast in oblast_rows:
    link = oblast.find("a")
    oblasts.append({"name": link.text, "link": link["href"]})

hromadas = []

for oblast in oblasts:
    if oblast["name"] == 'місто Київ':
        # todo kyiv is an edge case
        continue

    req = session.get("https://decentralization.gov.ua" + oblast["link"] + "/gromadu")
    all_hromadas_raw = BeautifulSoup(req.content, "html.parser")
    hromada_rows = all_hromadas_raw.find(id="communities").find_all("div", class_="community-table")

    gromada_regions_info = session.get("https://gromada.info/region/" + oblast["name"].replace(" ", "-"))
    gromada_regions_raw = BeautifulSoup(gromada_regions_info.content, "html.parser")
    gromada_regions = gromada_regions_raw.find(id="small_paragraph").find_all("p")[3].find_all("a")

    gromada_links = []
    for gromada_region in gromada_regions:
        gromada_region_name = gromada_region.text
        gromada_region_link = gromada_region["href"]
        gromada_region_link_list_raw = BeautifulSoup(session.get("https://gromada.info" + gromada_region_link).content,
                                                     "html.parser")
        gromada_region_link_list_ps = gromada_region_link_list_raw.find("main").find_all("p")
        for p in gromada_region_link_list_ps:
            if "Громади, що входять в" in p.text:
                gromada_region_link_list = p.find_all("a")

        # gromada_region_link_list = gromada_region_link_list_raw.find("main").find_all("p")[5].find_all("a")
        for gromada_link in gromada_region_link_list:
            gromada_links.append({"name": gromada_link.text.replace("’", "'").lower(), "link": gromada_link["href"]})

    oblast_hromadas = []
    for hromada in hromada_rows:
        # print("\n\n\n\n")
        # print(hromada)
        title = hromada.find("a").text
        rayon = hromada.find("div", {"title": "Район"}).text.strip()
        type = hromada.find("div", {"title": "Тип громади"}).text.strip()
        towns = hromada.find("div", {"title": "Кількість населених пунктів"}).text.strip()
        area = hromada.find("div", {"title": "Площа територіальної громади, кв.км"}).text.strip()
        population = hromada.find("div", {"title": "К-ть населення"}).text.strip()
        year = hromada.find("div", {"title": "Створена "}).text.strip()

        gromada_title = title.replace(" територіальна громада", " громада").replace("’", "'").lower()
        # {'name': 'Мар’янівська громада', 'link': '/gromada/maryanivska/'}
        # "Мар'янівська громада"
        # {'name': 'Верхівцевська громада', 'link': '/gromada/verhivcivska/'}
        if gromada_title == 'верхівцівська громада' and rayon == 'Кам’янський район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "верхівцевська громада"][0][
                "link"]
        elif gromada_title == 'райгородська громада' and rayon == 'Бердичівський район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "райгородоцька громада"][0][
                "link"]
            # {'name': 'райгородоцька громада', 'link': '/gromada/raygorodocka/'}
        elif gromada_title == 'дубриницько-малоберезнянська громада' and rayon == 'Ужгородський район':
            gromada_link = \
            [gromada for gromada in gromada_links if gromada["name"] == "дубриницько-малоберезня громада"][0]["link"]
            # {'name': 'дубриницько-малоберезня громада', 'link': '/gromada/dubrynycka/'}

        elif gromada_title == 'більмацька громада' and rayon == 'Пологівський район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "кам'янська громада"][0]["link"]
            # {'name': "кам'янська громада", 'link': '/gromada/bilmacka/'}

        elif gromada_title == 'новояворівська громада' and rayon == 'Яворівський район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "новояричівська громада"][0][
                "link"]
            # {'name': 'новояричівська громада', 'link': '/gromada/novoyarychiv/'}

        elif gromada_title == 'криниченська громада' and rayon == 'Болградський район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "криничненська громада"][0][
                "link"]
            # {'name': 'криничненська громада', 'link': '/gromada/krynychenska/'}

        elif gromada_title == 'диканьська громада' and rayon == 'Полтавський район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "диканська громада"][0]["link"]
            # {'name': 'диканська громада', 'link': '/gromada/dykanska/'}

        elif gromada_title == 'веренчацька громада' and rayon == 'Чернівецький район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "веренчанська громада"][0][
                "link"]
            # {'name': 'веренчанська громада', 'link': '/gromada/verenchanska/'}

        elif gromada_title == 'карапачівська громада' and rayon == 'Чернівецький район':
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == "карапчівська громада"][0][
                "link"]
            # {'name': 'карапчівська громада', 'link': '/gromada/karapchivska/'}
        else:
            gromada_link = [gromada for gromada in gromada_links if gromada["name"] == gromada_title][0]["link"]

        # {'name': "Кам'янська громада", 'link': '/gromada/kamjanska/'}

        # returns 404 for some reason
        if gromada_link == "/gromada/borschivska/":
            continue

        gromada_info_raw = BeautifulSoup(session.get("https://gromada.info" + gromada_link).content, "html.parser")
        # {'name': 'борщівська громада', 'link': '/gromada/borschivska/'}
        gromada_info_creation = gromada_info_raw.find("main").find_all("p")[0].text.strip().split(':')[
            1].strip().replace("р.", "")
        # gromada_info_consists_of = list(map(lambda a: a.text, gromada_info_raw.find("main").find_all("p")[3].find_all("a")))
        gromada_info_consists_of = list(
            map(lambda a: a.find("h3").find("span").text.strip().split(",")[0].replace("(", ""),
                gromada_info_raw.find("main").find_all("div", class_="ext_objects")))

        obj = {
            "Область": oblast["name"],
            "Район": rayon,
            "Назва": title,
            "Категорія": type,
            "Рік": year,
            "Кількість населених пунктів": towns,
            "Площа": area,
            "Населення": population,
            "Створена": gromada_info_creation,
            "Кількість рад у 2020 році": len(gromada_info_consists_of),
            "Перелік всіх рад у 2020 році": ", ".join(gromada_info_consists_of),
        }
        oblast_hromadas.append(obj)
        # print(obj)
        # break

    oblast_hromadas = sorted(oblast_hromadas, key=operator.itemgetter('Район', 'Назва'))
    hromadas.extend(oblast_hromadas)
    print(oblast["name"])
    # break?

# print(hromadas)


csv_file = "hromadas.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Область", "Район", "Назва", "Категорія", "Рік",
                                                     "Кількість населених пунктів", "Площа", "Населення", "Створена",
                                                     "Кількість рад у 2020 році",
                                                     "Перелік всіх рад у 2020 році", ])

        writer.writeheader()
        for data in hromadas:
            writer.writerow(data)
except IOError:
    print("I/O error")

print("All Done!")

