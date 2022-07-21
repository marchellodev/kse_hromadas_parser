import os
import re

from bs4 import BeautifulSoup

docs_dir = "tmp"
doc_files = [f for f in os.listdir(docs_dir) if f.endswith(".html") and os.path.isfile(os.path.join(docs_dir, f))]

for file in doc_files:
    print(file)
    f = open(os.path.join(docs_dir, file), "r").read()
    f_tbodies = BeautifulSoup(f, "html.parser").find("table").find_all("tbody")

    for tbody in f_tbodies:
        f_rows = tbody.find_all("tr")
        for row in f_rows:
            columns = row.find_all("td")
            name = columns[0].text.strip()
            hromadas = columns[3].text.strip()
            # todo sanitize parentheses properly instead of just removing them
            # https://stackoverflow.com/a/66901178
            hromadas = "".join(re.split("\(|\)|\[|\]", hromadas)[::2])

            while '\n\n' in hromadas or '\t' in hromadas:
                hromadas = hromadas.replace('\n\n', '\n')
                hromadas = hromadas.replace('\t', '')

            print(name)

    print("FILE DONE\n\n\n")
    # break
