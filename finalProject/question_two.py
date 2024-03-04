import pymongo
import requests

# connect to the client
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["itunes"]

# this is outside the if since we'll use it outside it
uk_songs = mydb["top100uk"]

# if the collection doesn't exist, create it
collection_list = myclient.get_database("itunes").list_collection_names()
if "top100uk" not in collection_list:
    # get the api's json contents into a variable
    url = "https://rss.applemarketingtools.com/api/v2/gb/music/most-played/100/songs.json"
    response = requests.get(url)

    # store the json in a variable
    data = response.json()

    # the real data is in the results array
    myList = data['feed']['results']
    uk_songs.insert_many(myList)

# fetch us songs
us_songs = mydb["top100us"]

# make a cursor ish for uk songs
x = uk_songs.find()

# variable for same songs
same_songs = 0

string = ''
# for key, value in x[0].items():
#     print("\'{0}\': \'{1}\'".format(key,value))
# loop through each song in uk song chart
for data in x:
    # get it into a correct answer to be found
    for key, value in data.items():
        string += "\'{0}\': \'{1}\', ".format(key, value)
    string = string[:-2]
    string = '{', string, '}'

    # only need to find one, will return None
    # (equivalent of null) if not found
    if us_songs.find_one(string) is not None:
        same_songs += 1

print("There are", same_songs, "songs that chart on both",
      "the top 100 for the US and UK charts")