import requests

# putting url together
beginning = "https://api.penguinrandomhouse.com/resources/v2/title/domains/PRH.US/"
api_key = "?api_key=6m9jsapwr6b4stqtanpt9kzu"
middle = "titles/"
isbn = ""   # put an isbn here

# basically somehow you'd have to loop the isbns you get and getting info
# from each new url for each random house work

url = beginning + middle + api_key
print(url)

response = requests.get(url)
print(response) # 200 is good

data = response.json()
print(data)

# make sure to ask for help or look in the google folder
# for my python file if you need help in connecting and executing and stuff