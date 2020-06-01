import urllib
import urllib2
import json


class FlickrLib:

    root_url = "https://www.flickr.com/services/rest/"
    dic = {}
    head = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36"}
    data = {"method": "flickr.photos.getInfo",
            "api_key": "2f145a0539ede4df69c6988b122f3cea",
            "photo_id": 0,
            "secret": "5fe5297177e0aa8f",
            "format": "json",
            "nojsoncallback": 1}

    @staticmethod
    def get_descripttion(photo_id):
        data = FlickrLib.data.copy()
        data["photo_id"] = photo_id
        data = urllib.urlencode(data).encode('utf-8')
        req = urllib2.Request(FlickrLib.root_url, data, FlickrLib.head)
        response = urllib2.urlopen(req)
        resp_text = response.read().decode('utf-8')
        # print(text)

        info_dic = json.loads(resp_text)

        # print(info_dic["stat"])
        # print(info_dic["photo"].keys())
        # print(info_dic["photo"]["description"]["_content"])

        if info_dic["stat"] != "ok":
            return ""
        descripttion = info_dic["photo"]["description"]["_content"]

        return descripttion


if __name__ == '__main__':
    text = FlickrLib.get_descripttion("15023708648")
