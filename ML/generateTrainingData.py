# importing module 
from pymongo import MongoClient 
import math
import json
import os.path
from os import path
from bson.json_util import dumps
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def generateTrainingData():
	# creation of MongoClient 
	client=MongoClient() 
  
	# Connect with the portnumber and host 
	client = MongoClient('mongodb://localhost:27017/') 
  
	# Access database 
	mydatabase = client["local"]
	mycollection = mydatabase["data_new5"]

	# query to filter all images whose MBR has atleast one corner that falls within the bounding box of the quadrant
	# query should also include if any corner of quadrant MBR is inside  the Image MBR (reverse the query)
	
	#query={"$and":[{"latitude":{"$gt":str(lats[1])}} , {"latitude":{"$lt":str(lats[0])}}, {"longitude":{"$gt":str(longs[0])}}, {"longitude":{"$lt":str(longs[1])}}]}
	#query={"$and":[{"latitude":{"$gt":"-85.0511287798"}} , {"latitude":{"$lt":"85.0511287798"}}, {"longitude":{"$gt":"-180.0"}}, {"longitude":{"$lt":"180.0"}}]}
	
	result=[]
	query = {"keyword":"Sydney"}
	# Access collection of the database to filter results based on query
#	result.append(mycollection.find(query))
	result1=mycollection.find(query)\
	
#	JSONEncoder().encode(result1)
	#with open('imagesToScore.json', 'w') as outfile:
        #	json.dump(result, outfile)
	#	print("success!")
	#with open('imagesToScore.json', 'w') as outfile:
	#	json.dump(list(result1), outfile)
 
	for record1 in result1:
		print(record1)
		del record1['_id']
		result.append(record1)
		#print(record1)
		#box = record1["box"]
		#print(box[0])
		#calculate score
		views=int(record1["views"])
		comments=int(record1["comments"])
		favorites=int(record1["favorites"])
		id=record1["id"]
		value=(views/10)*3+(favorites/10)*2+(comments/10)*2
	
	with open('imagesToScore.json', 'w') as outfile:
                json.dump(result, outfile)
                print("success!")
generateTrainingData()
 
