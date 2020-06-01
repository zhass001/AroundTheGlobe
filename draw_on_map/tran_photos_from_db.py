from shutil import copyfile
import os
import json
import urllib.request
from match_pic_lib import *
from origin_match_pic_lib import *
import time


def low_level_pos(pos):
    dw_pos_li = []
    z, x, y = pos
    nz, nx, ny = z + 1, x * 2, y * 2
    for dx in [0, 1]:
        for dy in [0, 1]:
            dw_pos_li.append((nz, nx + dx, ny + dy))
    return dw_pos_li


def tran_pic(pic_list, del_f, s_log):
    print("downloading/copying photos")
    if not os.path.exists(pic_root):
        os.mkdir(pic_root)
    with open(pic_dic_path, "w", encoding="utf-8")as f:
        json.dump(pic_list, f)

    if del_f:
        file_li = os.walk(pic_root)
        # print(file_li)
        for dir_li in file_li:
            (root, dirs, files) = dir_li
            for file in files:
                # print(root,file)
                path = os.path.join(root, file)
                # print(path)
                if path.endswith("png"):
                    if s_log:
                        print("del", path)
                    os.remove(path)

    for pos, url in pic_list:
        name = "tile-%d-%d-%d.png" % pos
        new_path = os.path.join(pic_root, name)
        if s_log:
            print(url, new_path)

        if url:
            try:
                urllib.request.urlretrieve(url, new_path)
            except Exception as e:
                print(e)
        pic_dic = {x[0] for x in pic_list}
        for ll_pos in low_level_pos(pos):
            if ll_pos not in pic_dic:
                name = "tile-%d-%d-%d.png" % ll_pos
                new_path = os.path.join(pic_root, name)
                copyfile(empyt_pic_path, new_path)


if __name__ == '__main__':
    pic_dic_name = "pic_dic.json"
    empyt_pic_path = "./empty.png"
    pic_root = "./data"

    # path to save match result in jason format
    pic_dic_path = os.path.join(pic_root, pic_dic_name)

    # delete photos in the pic_root
    delete_file = True
    # show log of download/copy photos
    show_log = False

    z_min = 0
    z_max = 0
    z_range = range(z_min, z_max+1)
    print(z_range)

    #MatchPhotos is for new one / MatchPhotosOrigin is the old one
    #mp = MatchPhotos()
    mp = MatchPhotosOrigin()

    # set threshold for area
    mp.threshold = 0

    # Connect with the portnumber and host
    mp.client = MongoClient('mongodb://localhost:27017/')
    mp.mydatabase = mp.client["local"]
    mp.mycollection = mp.mydatabase["data_new9"]

    # match photos
    start_time = time.time()
    pic_list = mp.match_pic(z_range)
    print("photo number: %d" % len(pic_list))
    used_time = time.time() - start_time
    print("used time: %fs" % used_time)

    # copy photos
    start_time = time.time()
    tran_pic(pic_list, delete_file, show_log)

    used_time = time.time() - start_time
    print("used time: %fs" % used_time)
