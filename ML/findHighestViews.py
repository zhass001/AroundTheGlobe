# importing module 
from pymongo import MongoClient 
import math
import json
import os.path
from os import path
from bson.json_util import dumps

def findHighestViews():
	# creation of MongoClient 
	client=MongoClient() 
  
	# Connect with the portnumber and host 
	client = MongoClient('mongodb://localhost:27017/') 
  
	# Access database 
	mydatabase = client["local"]
	mycollection = mydatabase["data_new9"]
	#query = {$max: "$quantity"}
	# Access collection of the database to filter results based on query
	#result1=mycollection.find({"keyword":"Paris"}).sort("views", 1)
        result1=mycollection.find({"keyword":"Paris", "country":"France"}).sort("views",-1)
	print(result1[2])
	#for record1 in result1:
		#print(record1)

findHighestViews()
 
