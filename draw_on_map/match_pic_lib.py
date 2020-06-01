from pymongo import MongoClient
from collections import namedtuple
import math


class MatchPhotos:
    threshold = None
    mycollection = None

    def __init__(self):
        self.pic_list = []

    def numTodeg(self, xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)

    def findArea(self, x1min, y1min, x1max, y1max, x2min, y2min, x2max, y2max):
        Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

        a = Rectangle(x1min, y1min, x1max, y1max)
        b = Rectangle(x2min, y2min, x2max, y2max)

        dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
        dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
        if (dx >= 0) and (dy >= 0):
            return dx * dy

    def gentiles(self, zoom):
        t = 0
        for i in range(0, 2 ** zoom):
            for j in range(0, 2 ** zoom):
                t += 1
                result_north_west = self.numTodeg(i, j, zoom)
                result_south_east = self.numTodeg(i + 1, j + 1, zoom)
                lats = [result_north_west[0], result_south_east[0]]  # north,south
                longs = [result_south_east[1], result_north_west[1]]  # east, west

                # print("                      ")
                # print("                      ")
                # print("                      ")
                # print("For quadrant" + str(t))
                # print("                      ")
                # print("                      ")
                # print("                      ")
                # print(lats, longs)
                pic_url = self.findLocations(lats, longs, i, j)
                if pic_url:
                    pos = (zoom, i, j)
                    self.pic_list.append([pos, pic_url])

    def findLocations(self, lats, longs, i, j):
        # threshhold for the area

        # query to filter all images whose MBR has atleast one corner that falls within the bounding box of the quadrant
        # query should also include if any corner of quadrant MBR is inside  the Image MBR (reverse the query)

        # query={"$and":[{"latitude":{"$gt":str(lats[1])}} , {"latitude":{"$lt":str(lats[0])}}, {"longitude":{"$gt":str(longs[0])}}, {"longitude":{"$lt":str(longs[1])}}]}
        # query={"$and":[{"latitude":{"$gt":"-85.0511287798"}} , {"latitude":{"$lt":"85.0511287798"}}, {"longitude":{"$gt":"-180.0"}}, {"longitude":{"$lt":"180.0"}}]}

        query = {"$nor": [{"box.2": {"$lt": longs[1]}}, {"box.3": {"$gt": longs[0]}},
                          # box.2 > box.3; logns[0] > longs[1]
                          {"box.0": {"$lt": lats[1]}}, {"box.1": {"$gt": lats[0]}},
                          # box.0 > box.1; lats[0] > lats[1]
                          ]}

        # Access collection of the database to filter results based on query
        result1 = self.mycollection.find(query)

        value = 0
        url = None
        for record1 in result1:
            if not record1["box"] or not record1["url"]:
                continue
            # print(record1["box"], lats+longs)
            # print(record1)
            views = int(record1["views"])
            comments = int(record1["comments"])
            favorites = int(record1["favorites"])
            id = record1["id"]
            # print(record1)
            box = record1["box"]
            url_n = record1["url"]
            # print(box[0])
            # calculate score
            area = 0
            value_n = 0
            if box != None:
                area = self.findArea(float(lats[1]), float(longs[1]), float(lats[0]), float(longs[0]), float(box[1]),
                                     float(box[3]), float(box[0]), float(box[2]))
                if area is None or area < self.threshold:
                    value_n = 0
                else:
                    value_n = (views*0.00000873685492445) + (favorites*0.0058143326847) + (comments* 0.011241175104) + (area / 10)

            if value_n > value:
                value = value_n
                url = url_n
        return url

    def match_pic(self, z_range):
        for zoom in z_range:
            self.gentiles(zoom)
        return self.pic_list
