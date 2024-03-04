import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

# use the database
mydb = myclient["itunes"]
# use the collection
us_songs = mydb["top100us"]

# put all the fields in a variable
# x is a list (cursor) of all "rows"
x = us_songs.find()

# the variable we'll use to count how many country songs
country_songs = 0

# loop through all entries in the cursor
for data in x:
    # data is a dictionary, we use .get and we
    # get the array of genres
    genres = data.get('genres')

    # loop through the array of genres
    for genre in genres:
        # search for the country genre name
        if genre['name'] == 'Country':
            country_songs += 1

print('There are', country_songs, 'country songs')