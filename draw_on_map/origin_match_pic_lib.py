import math
import numpy as np
import json
import csv

class MatchPhotosOrigin:
    threshold = None
    mycollection = None
    def __init__(self):
        pass

    def judge_inter(self, box1, box2):

        n1, s1, e1, w1 = box1
        n2, s2, e2, w2 = box2

        lx = abs((e1 + w1) / 2 - (e2 + w2) / 2)
        ly = abs((n1 + s1) / 2 - (n2 + s2) / 2)
        sax = abs(e1 - w1)
        sbx = abs(e2 - w2)
        say = abs(n1 - s1)
        sby = abs(n2 - s2)
        if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
            return True
        else:
            return False

    def solve_coincide(self, box1, box2):
        n1, s1, e1, w1 = box1
        n2, s2, e2, w2 = box2
        if self.judge_inter(box1, box2):
            col = min(e1, e2) - max(w1, w2)
            row = min(n1, n2) - max(s1, s2)
            intersection = col * row
            area1 = abs(w1 - e1) * abs(s1 - n1)
            area2 = abs(w2 - e2) * abs(s2 - n2)
            # print(area1,area2,intersection)
            coincide = intersection / (area1 + area2 - intersection)
            return coincide
        else:
            # print(box1, box2)
            return 0


    def num2deg_y(self, y, z):
        y_n = np.pi * (1 - 2* y / (2**z))
        rad = np.arctan(np.sinh(y_n))
        return rad * 180 / np.pi

    def num2deg_x(self, x,z):
        return -180 + x / (2**z)*360

    def deg2num(self, lat_deg, lon_deg, zoom):
      lat_rad = math.radians(lat_deg)
      n = 2.0 ** zoom
      xtile = int((lon_deg + 180.0) / 360.0 * n)
      ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
      return (xtile, ytile)


    def gen_box(self, z_range):

        box_dic = {}
        for z in z_range:
            w = 2**z
            for x in range(w):
                for y in range(w):
                    box_dic[(z,x,y)] = [self.num2deg_y(y, z), self.num2deg_y(y + 1, z), self.num2deg_x(x + 1, z), self.num2deg_x(x, z)]
        return box_dic


    def find_overlap(self, item_dic, z_range):
        box_li = []
        if item_dic["box"] and item_dic["url"]:
            pic_box = [float(x) for x in item_dic["box"]]
            n, s, e, w = pic_box
            for z in z_range:
                max_x, max_y = self.deg2num(lat_deg=n, lon_deg=e, zoom=z)
                min_x, min_y = self.deg2num(lat_deg=s, lon_deg=w, zoom=z)
                # print(pic_box, min_x, max_x, min_y, max_y)
                for x in range(max(0, min_x-1), min(2**z, max_x+2)):
                    for y in range(max(0, min_y-1), min(2**z, max_y+2)):
                        box_li.append((z, x, y))
        return box_li

    def eval_pic(self, box, item_dic):
        score = 0
        if item_dic["box"] and item_dic["url"]:
            pic_box = [float(x) for x in item_dic["box"]]
            sim = self.solve_coincide(box, pic_box)
	    #print(sim)
            if sim > self.threshold:
                views = int(item_dic["views"])
                comments = int(item_dic["comments"])
                favorites = int(item_dic["favorites"])
                score = ((views*0.000014917925134072991) + (favorites*0.00046668832671921336)+ (comments*0.005669643190465376))* sim 
        #print("For views: "+str(item_dic["views"])+",favs: "+str(item_dic["favorites"])+",comments: "+str(item_dic["comments"]))
        return score

    def match_pic(self, z_range):
        box_dic = self.gen_box(z_range)

        # pic list to return (pos. url)
        pic_list = []
        # tmp dic to save pic candidates for each tiles
        tmp_pic_dic = {}
        # a set for check dup pic
        url_dic = set()

        result = self.mycollection.find()
        for item_dic in result:
            box_li = self.find_overlap(item_dic, z_range)
            # print(box_li)
            for pos in box_li:
                box = box_dic[pos]
                score = self.eval_pic(box, item_dic)
                #print("Score is:"+str(score))
                if score:
                    url = item_dic["url"]
                    if pos not in tmp_pic_dic:
                        tmp_pic_dic[pos] = [[score, url]]
                    else:
                        tmp_pic_dic[pos].append([score, url])
        #print(tmp_pic_dic)
        #with open('tmp_pic_dic.txt', 'w') as outfile:
            #json.dump(tmp_pic_dic, outfile)
        w = csv.writer(open("output.csv", "w"))
        for key, val in tmp_pic_dic.items():
            w.writerow([key, val])
        for pos, pic_li in tmp_pic_dic.items():
            z,x,y = pos 
            score = 0
            url = None
            for pic_info in pic_li:
                score_n, url_n = pic_info
                if (url_n,z) not in url_dic and score_n > score:
                    score = score_n
                    url = url_n
            if url:
                pic_list.append([pos, url])
                url_dic.add((url,z))
            else:
                print(pos)

        return pic_list




