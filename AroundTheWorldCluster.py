def crawlFlickr(keywords):
    dataCity = []
    dataCountry = []
    dataCounty = []
    dataProvince = []
    if (path.exists('data_City.json')):
        print("found existing city.json! Reading it!")
        with open('data_City.json') as json_file1:
            dataCity = json.load(json_file1)
    if (path.exists('data_Country.json')):
        print("found existing country.json! Reading it!")
        with open('data_Country.json') as json_file2:
            dataCountry = json.load(json_file2)
    if (path.exists('data_County.json')):
        print("found existing county.json! Reading it!")
        with open('data_County.json') as json_file3:
            dataCounty = json.load(json_file3)
    if (path.exists('data_Province.json')):
        print("found existing province.json! Reading it!")
        with open('data_Province.json') as json_file4:
            dataProvince = json.load(json_file4)
    
    for keyword in keywords:
        print("Current Point is:")
        print(keyword)
        photos = []
        time.sleep(5)
        now=datetime.now()
        minUploadDate = now.strftime("%m/%d/%Y %H:%M:%S")
        if zoomLevel=="City":
            for eachPoint in dataCity:
                if(eachPoint['keyword']==keyword):
                    minUploadDate = eachPoint["download_time"]
        elif zoomLevel=="Country":
            for eachPoint in dataCountry:
                if (eachPoint["keyword"] == keyword):
                    minUploadDate = eachPoint["download_time"]
        elif zoomLevel=="County":
            for eachPoint in dataCounty:
                if(eachPoint['keyword']==keyword):
                    minUploadDate = eachPoint["download_time"]
        elif zoomLevel=="Province":
            for eachPoint in dataProvince:
                if(eachPoint['keyword']==keyword):
                    minUploadDate = eachPoint["download_time"]
        try:
            photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         tags=keyword,
                         extras='views, url_c, comments, favorites',          # may be you can try different numbers..
                         sort='relevance',
                         has_geo = '1')
        except flickrapi.exceptions.FlickrError as e:
            print("Caught an Exception in Location:!")
            print(keyword)
            raise Error(e)
            print(e)
	  
        comments=0
        countPhotos=0

        for i, photo in enumerate(photos):
            idExists=0
            id = photo.get('id')
            #check if the ID already exists in the json
            for eachPoint in dataCity:
                if(eachPoint["id"]==id):
                    idExists=1
            for eachPoint in dataCountry:
                if (eachPoint["id"] == id):
                    idExists = 1
            for eachPoint in dataCounty:
                if (eachPoint["id"] == id):
                    idExists = 1
	    for eachPoint in dataProvince:
                if (eachPoint["id"] == id):
                    idExists = 1
            #if id does not exist, go ahead
            if(idExists==0):
                pair = {}
                #to make sure we have the json format intact, even if an exception occurs in the middle
                pair["url"]=""
                pair["views"]=""
                pair["keyword"]=""
                pair["favorites"]=""
                pair["comments"]=""
                pair["zoomLevel"]=""
                pair["name"]=""
                pair["id"]=""
                pair["localId"]=""
                pair["description"] = ""
                pair["locality"]=""
                pair["region"]=""
                pair["country"] = ""
                pair["neighbourhood"] = ""
                pair["latitude"]=""
                pair["longitude"]=""

                url = photo.get('url_c')
                name = ""
                #get views, favorites, description, comments and location(locality, region, neighborhood, country)
                views = photo.get('views')
                favorites = flickr.photos_getFavorites(photo_id=id)
                desc = FlickrLib.get_descripttion(id)
                location = FlickrLibLoc.get_location(id)
                countfaves=favorites.find('photo').get('total')
                comments=flickr.photos_comments_getList(photo_id=id)
                countcomments=len(comments.findall('.//comment'))
                #time.sleep(1)
                name = keyword+str(id)+'.jpg'
                pair["url"]=url
                pair["views"]=views
                pair["favorites"]=countfaves
                pair["comments"]=countcomments
                pair["zoomLevel"]=zoomLevel
                pair["name"]=name
                pair["id"]=id
                pair["localId"]=keyword+str(i)
                try:
                    pair["description"] = desc
                    pair["locality"]=location["locality"]
                    pair["region"]=location["region"]
                    pair["country"] = location["country"]
                    pair["neighbourhood"] = location["neighbourhood"]
                    pair["latitude"]=location["latitude"]
                    pair["longitude"]=location["longitude"]
                except:
                    print("Caught an Exception in Location:!")
                    print(keyword)
                now=datetime.now()
                dateTime = now.strftime("%m/%d/%Y %H:%M:%S")
                pair["download_time"] = dateTime
                pair["keyword"] =  keyword

                if zoomLevel=="City":
                    dataCity.append(pair)
                    with open('data_' + zoomLevel + '.json', 'w') as outfile:
                      #dump collected data in json file
                      json.dump(dataCity, outfile)
                    print(keyword+": appended successfully!")
                if zoomLevel=="Country":
                    dataCountry.append(pair)
                    with open('data_' + zoomLevel + '.json', 'w') as outfile:
                      #dump collected data in json file
                      json.dump(dataCountry, outfile)
                    print(keyword + ": appended successfully!")
                if zoomLevel=="County":
                    dataCounty.append(pair)
                    with open('data_' + zoomLevel + '.json', 'w') as outfile:
                      #dump collected data in json file
                      json.dump(dataCounty, outfile)
                    print(keyword + ": appended successfully!")
                if zoomLevel=="Province":
                    print("I will write to file province")
                    dataProvince.append(pair)
                    with open('data_' + zoomLevel + '.json', 'w') as outfile:
                      #dump collected data in json file
                      json.dump(dataProvince, outfile)
                    print(keyword+": appended successfully!")

                urls.append(pair)
                countPhotos = countPhotos + 1
                # get 10 images per keyword
                if i > 10:
                    break


        print("new photos for "+keyword+" are:")
        print(countPhotos)
        # Download image from the url and save it to '<name>.jpg'
        n=len(urls)
        for j in range(0, n):
            if urls[j]['url'] != None:
                urllib.urlretrieve(urls[j]["url"], urls[j]["name"])
                image = Image.open(urls[j]["name"])
                saveName = urls[j]["name"]
                #image = image.resize((256, 256), Image.ANTIALIAS)
                image.save(saveName)
            else:
                name = None
                urls[j]["name"]=name
                j=j+1

  #with open('data_' + zoomLevel + '.json', 'w') as outfile:
    #if zoomLevel == "City":
      #json.dump(dataCity, outfile)
    #if zoomLevel == "Country":
      #json.dump(dataCountry,outfile)

	#empty keywords
    keywords=[]



import flickrapi
import urllib
from PIL import Image
import json
import os.path
from os import path
import time
from datetime import datetime
from xml.dom import minidom
from flickr_lib import *
from getLocation import *

# Flickr api access key of Zoama Hassan
flickr=flickrapi.FlickrAPI('cdb5888830de9d064820bbd62bc198af', '24979cce607d1887', cache=True)


zoomLevel=""
keywords=[]
urls = []
while(1==1):
    #reading query text file
    query_file_name = 'citiesInTheWorldEleven.txt'
    query_file = open(query_file_name, 'r')
    for line in query_file:
        print("we are reading query file again")
        lineText = line[0:len(line) - 1]
        if lineText == "Cities":
            urls = []
            zoomLevel = "City"
	    print("Found cities")
            print(lineText)
            continue
	elif lineText == "Counties":
	    urls = []
            print("Found counties")
            zoomLevel == "County"
	    print(lineText)
        elif lineText == "Countries":
            urls = []
            zoomLevel = "Country"
            print(lineText)
            continue
        elif lineText == "Provinces":
            urls = []
            zoomLevel = "Province"
            print(lineText)
            continue
        else:
            if lineText == "--end--":
                print(lineText)
                try:
                    crawlFlickr(keywords)
                except flickrapi.exceptions.FlickrError as e:
                    print("Caught an exception")
                    print("running program again")
                    crawlFlickr(keywords)
                keywords = []
            else:
                print(lineText)
                print(zoomLevel)
                #append keyword to keywords list
                keywords = keywords + [line[0:len(line) - 1]]

