package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/JamesMilnerUK/pip-go"
	"github.com/paulmach/osm"
	"github.com/paulmach/osm/osmpbf"
	"github.com/gocarina/gocsv"
	"io/ioutil"
	"log"
	"os"
	"runtime"
)

type MapList []MapHromada

type MapHromada struct {
	Name    string      `json:"name"`
	Region  string      `json:"region"`
	Oblast  string      `json:"oblast"`
	Polygon [][]float64 `json:"polygon"`
}

type ResultRecord struct {
	Hromada string `json:"name"`
	Region  string `json:"region"`
	Oblast  string `json:"oblast"`

	Coordinates []float64
	Tags        string
	OsmId       int64
}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())

	// parse out all the maps
	var maps MapList

	content, err := ioutil.ReadFile("./map.json")
	if err != nil {
		log.Fatal("Error when opening file: ", err)
	}

	// Now let's unmarshall the data into `payload`
	err = json.Unmarshal(content, &maps)
	if err != nil {
		log.Fatal("Error during Unmarshal(): ", err)
	}

	file, err := os.Open("ukraine-latest.osm.pbf")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// The third parameter is the number of parallel decoders to use.
	scanner := osmpbf.New(context.Background(), file, runtime.GOMAXPROCS(-1))
	defer scanner.Close()

	//var results []ResultRecord
	ch := make(chan ResultRecord)

	responses := 0
	//out:
	for scanner.Scan() {

		switch o := scanner.Object().(type) {
		case *osm.Node:

			if o.Tags.Find("amenity") != "" {
				responses += 1
				pt1 := pip.Point{X: o.Lat, Y: o.Lon}

				go func(ch chan<- ResultRecord) {
					responded := false

					for _, el := range maps {

						var points []pip.Point
						for _, p := range el.Polygon {
							points = append(points, pip.Point{X: p[0], Y: p[1]})
						}

						rectangle := pip.Polygon{
							Points: points,
						}

						inPolygon := pip.PointInPolygon(pt1, rectangle) // Test - Should return true

						if inPolygon {
							var tags string
							for _, t := range o.Tags {
								tags += t.Key + "=" + t.Value + ","
							}

							ch <- ResultRecord{
								Hromada:     el.Name,
								Region:      el.Region,
								Oblast:      el.Oblast,
								Coordinates: []float64{o.Lat, o.Lon},
								Tags:        tags,
							}
							responded = true

							//fmt.Println(el.Name, el.Region, el.Oblast)
							//runtime.Breakpoint()
							//break out
						}

						//ch <- result{task: task, data: task * 2, err: nil}
					}
					if !responded {
						ch <- ResultRecord{
							Hromada:     "",
							Region:      "",
							Oblast:      "",
							Coordinates: []float64{o.Lat, o.Lon},
							Tags:        "",
						}
					}
				}(ch)

			}

		case *osm.Way:
			// city name
			// city nodes

			if o.Tags.Find("boundary") == "administrative" {
				//fmt.Println(o.Tags.Find("admin_level"))
				//runtime.Breakpoint()
				//interesting_nodes = o.Nodes.NodeIDs()
				break
			}

		case *osm.Relation:
			//fmt.Println("Relation")
		}

	}

	fmt.Println(responses)
	//results := make([]ResultRecord, responses)
	var results []ResultRecord

	for i := 0; i < responses; i++ {
		r := <-ch

		if r.Hromada != "" && r.Region != "" && r.Oblast != "" {
			results = append(results, r)
		}
	}

	fileOut, err := ioutil.TempFile(".", "results-*.csv")
	if err != nil {
		panic(err)
	}
	defer fileOut.Close()

	err = gocsv.MarshalFile(&results, fileOut)
	if err != nil {
		panic(err)
	}
	fmt.Println("DONE")
}
