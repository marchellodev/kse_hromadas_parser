"""
Search for pubs in an osm file and list their names.
"""
import osmium
import sys

class NamesHandler(osmium.SimpleHandler):

    def output_pubs(self, tags):
        a = 1
        # if tags.get('amenity') == 'pub' and 'name' in tags:
        #     print()

    def node(self, n):
        # print(dict(n))
        self.output_pubs(n.tags)

    def way(self, w):
        self.output_pubs(w.tags)

    def relation(self, w):
        self.output_pubs(w.tags)

    def area(self, w):
        self.output_pubs(w.tags)

def main(osmfile):
    NamesHandler().apply_file(osmfile)

    return 0

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: python %s <osmfile>" % sys.argv[0])
    #     sys.exit(-1)

    exit(main("ukraine-latest.osm.pbf"))
