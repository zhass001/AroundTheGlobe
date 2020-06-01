import json
import os


def add_coord():
    with open(loc_dic_path, 'r', encoding="utf-8")as f:
        loc_dic = json.load(f)

    with open(file_path, 'r', encoding="utf-8")as f:
        data_li = json.load(f)

    # print(data_li)
    for item_dic in data_li:
        new_item_dic = item_dic.copy()
        # print(item_dic)

        # if "path" not in item_dic:
        #     item_dic["path"] = None

        # keyword = item_dic["keyword"]
        if "region" in new_item_dic and "country" in new_item_dic:
            keyword = ", ".join([new_item_dic["keyword"], new_item_dic["region"], new_item_dic["country"]])
        else:
            keyword = new_item_dic["keyword"]

        # print(keyword, loc_dic[keyword])
        if loc_dic[keyword]:
            [cordinate, box, loc_type] = loc_dic[keyword]
            if "longitude" not in new_item_dic or "latitude" not in new_item_dic or not new_item_dic["longitude"] or not new_item_dic["latitude"]:
                new_item_dic["latitude"], new_item_dic["longitude"] = [float(x) for x in cordinate]
            else:
                new_item_dic["latitude"], new_item_dic["longitude"] = float(new_item_dic["latitude"]), float(
                    new_item_dic["longitude"])
            new_item_dic["box"] = [float(x) for x in box]
        else:
            if "longitude" not in new_item_dic or "latitude" not in new_item_dic:
                new_item_dic["latitude"], new_item_dic["longitude"] = [None] * 2
            new_item_dic["box"] = None
        if type(new_item_dic["views"]) != int:
            new_item_dic["views"] = int(new_item_dic["views"]) if type(new_item_dic["views"]) == str else 0
        if type(new_item_dic["comments"]) != int:
            new_item_dic["comments"] = int(new_item_dic["comments"]) if type(new_item_dic["comments"]) == str else 0
        if type(new_item_dic["favorites"]) != int:
            new_item_dic["favorites"] = int(new_item_dic["favorites"]) if type(new_item_dic["favorites"]) == str else 0

        # "longitude": "-71.347982", "favorites": "0", "download_time": "11/18/2019 14:42:11", "latitude": "42.460747"

        with open(new_file_path, 'a', encoding="utf-8")as f:
            s = json.dumps(new_item_dic).replace("\n", " ")
            # json.dump(s, f)
            f.write(s + "\n")


if __name__ == '__main__':
    zoomLevel_li = ["Country", "City", "County", "Province"]
    new_file_path = './DataForTiles/data_new.json'
    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    for zoomLevel in zoomLevel_li:
        file_path = './DataForTiles/data_%s.json' % zoomLevel
        loc_dic_path = "./DataForTiles/data_%s_loc.json" % zoomLevel
        add_coord()
