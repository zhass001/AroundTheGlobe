import urllib
import urllib2
import json


class FlickrLibLoc:

    root_url = "https://www.flickr.com/services/rest/"
    dic = {}
    head = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36"}
    data = {"method": "flickr.photos.geo.getLocation",
            "api_key": "2f145a0539ede4df69c6988b122f3cea",
            "photo_id": 0,
            "secret": "5fe5297177e0aa8f",
            "format": "json",
            "nojsoncallback": 1}

    @staticmethod
    def get_location(photo_id):
        data = FlickrLibLoc.data.copy()
        data["photo_id"] = photo_id
        data = urllib.urlencode(data).encode('utf-8')
        req = urllib2.Request(FlickrLibLoc.root_url, data, FlickrLibLoc.head)
        response = urllib2.urlopen(req)
        resp_text = response.read().decode('utf-8')
        # print(text)

        info_dic = json.loads(resp_text)

        #print(info_dic["stat"])

        if info_dic["stat"] != "ok":
            return ""

        loc_details = []
        loc = {}


        latitude = info_dic["photo"]["location"]["latitude"]
        loc["latitude"]=latitude
        longitude = info_dic["photo"]["location"]["longitude"]
        loc["longitude"] = longitude

        try:
            locality = info_dic["photo"]["location"]["locality"]["_content"]
            loc["locality"]=locality
        except:
            print("exception: no locality found")
        #if(info_dic["photo"]["location"]["region"]!=None):
        try:
            region = info_dic["photo"]["location"]["region"]["_content"]
            loc["region"] = region
        except:
            print("exception: no region found")
        #if(info_dic["photo"]["location"]["country"]!=None):
        try:
            country = info_dic["photo"]["location"]["country"]["_content"]
            loc["country"] = country
        except:
            print("exception: no country found")
        try:
            neighbourhood = info_dic["photo"]["location"]["neighbourhood"]["_content"]
            loc["neighbourhood"] = neighbourhood
        except:
            print("exception: no neighbourhood found")



        return loc


if __name__ == '__main__':
    text = FlickrLibLoc.get_location("15023708648")
