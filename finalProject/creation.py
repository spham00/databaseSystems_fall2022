# The link stored in the url variable was used
# This is because the one in the actual assignment didn't work

# pymongo is package used for MongoDB
import pymongo
# used to access APIs
import requests

# connect to the client
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["itunes"]

# check if the collections exist before creating them
dblist = myclient.list_database_names()
collection_list = myclient.get_database("itunes").list_collection_names()

# creating the US collection
if "top100us" not in collection_list:
    # get the api's json contents into a variable
    url = "https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json"
    response = requests.get(url)

    # make the collection for it, store the json in a variable
    us_songs = mydb["top100us"]
    data = response.json()

    # the real data is in the results array
    myList = data['feed']['results']
    us_songs.insert_many(myList)

# creating the UK collection
if "top100uk" not in collection_list:
    url = "https://rss.applemarketingtools.com/api/v2/gb/music/most-played/100/songs.json"
    response = requests.get(url)

    uk_songs = mydb["top100uk"]
    data = response.json()

    myList = data['feed']['results']
    uk_songs.insert_many(myList)

print("Collections have been created")