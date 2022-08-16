# Produced data

[List of hromadas in Ukraine](hromadas.csv) \
[List of youth centers in Ukraine](youth/centers/centers.csv) \
[List of youth radas in Ukraine](youth/radas/radas.csv) \
[List of business support centers in Ukraine](business_support.csv)
[List of businesses in Ukraine by hromadas](osm_go/results-1920954212.csv)

## Dependencies
```shell
pip3 install beautifulsoup4
pip3 install requests-cache
pip3 install pandas

# also golang: https://go.dev/
```

## Scripts in this repo
```shell
python3 hromadas_information.py
# Produces hromadas.csv - list of all hromadas in Ukraine
# Fetches data from decentralization.gov.ua and gromada.info

python3 hromadas_new.py
# Was supposed to parse files in the 2020-docs/ folder
# but was not finished since needed data was obtained directly

python3 youth/centers/parse.py
# Produces centers.csv - List of youth centers in Ukraine
# Fetches data from youthcenters.net.ua

python3 youth/radas/parse.py
# Produces radas.csv
# Fetches data from locations.csv
# locations.csv is locations.json transformed to the csv format
# json can be found in the source code of the map
# on the website youthcouncil.com.ua

# before running, download ukraine-latest.osm.pbf into the osm_go folder from https://download.geofabrik.de/europe/ukraine.html
cd osm_go
python3 hromadas.py # gets the list of maps of hromadas
go get # updates the go packages
go run main.go # runs the go script
# Produces list of businesses in Ukraine by hromada
# Note: The golang script may take up to 20 minutes to finish and will eat up all your cpu resources
```

### Resources used
> https://decentralization.gov.ua/areas - list of hromadas
> https://gromada.info - additional info about hromadas + hromada maps
> https://youthcenters.net.ua - list of youth centers
> https://youthcouncil.com.ua - map of youth councils

> https://auc.org.ua/novyna/opublikovano-23-rozporyadzhennya-pro-administratyvni-centry-ta-terytoriyi-terytorialnyh - radas that go into each hromada

> https://download.geofabrik.de/europe/ukraine.html - openstreetmap's data of Ukraine

To covert doc files to html use (libre office is needed):
```shell
lowriter --convert-to html 2020-docs/*.doc --outdir tmp
```
`Херсонської області.pdf` file is in the pdf format for some reason, so it should be processed manually