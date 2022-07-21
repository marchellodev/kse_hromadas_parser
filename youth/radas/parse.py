import csv
from bs4 import BeautifulSoup
import pandas as pd

file = open('locations.csv', newline='')
reader = csv.reader(file)

final_data = []

for line in reader:
    lat = line[0]
    long = line[1]
    code = line[2]
    code_parsed = BeautifulSoup(code, "html.parser")
    for div in code_parsed.find_all("div"):
        div.decompose()

    name = str(code_parsed).split("<br/>")[0]
    meta = str(code_parsed.text).replace(name, "")
    if code_parsed.find("a") is not None:
        link = code_parsed.find("a")["href"]
    # print(name)
    final_data.append({"lat": lat, "long": long, "name": name, "link": link, "meta": meta})
    # break

print(final_data)

df = pd.DataFrame(final_data)

# saving the dataframe
df.to_csv('radas.csv')
