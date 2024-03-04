import json
import requests

import mysql.connector
from mysql.connector import errorcode


def connect():
    try:
        mydb = mysql.connector.connect(
            # fill accordingly to your api
            host='127.0.0.1',
            user='root',
            password='',
            # database=dbase
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        mycursor = mydb.cursor()

    return mydb, mycursor


def get_openlibrary(isbn):
    url = 'https://openlibrary.org/search.json?isbn=' + isbn
    data = requests.get(url).json()['docs'][0]
    # useful fields: data['subject']
    return data


def get_googlebooks(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&key=AIzaSyDrFt3Wh8yXDtR-Na_IUSE3Vj-zZI9VNgE"
    response = requests.get(url)
    data = response.json()['items'][0]['volumeInfo']
    # useful fields: data['description'], data['average_rating']
    return data


def get_penguin(isbn):
    beginning = "https://api.penguinrandomhouse.com/resources/v2/title/domains/PRH.US/"
    api_key = "?api_key=6m9jsapwr6b4stqtanpt9kzu"
    middle = "titles/"  # put an isbn here

    url = beginning + middle + isbn + api_key

    data = requests.get(url).json()['data']['titles'][0]
    # useful fields: data['subjects']
    return data


def get_nytimes():
    # Setting up string for requesting info
    access_key = "qgSd60mPz5XAxiNttMJroiDMmKWMmN1B"
    secret_key = "vzwESl6P5JqBwtBZ"  # not sure if it's needed but putting heere
    keys = "?api-key=" + access_key
    url = "https://api.nytimes.com/svc/books/v3"
    # json = "/lists/2022-11-21/hardcover-fiction.json"
    json = "/lists/overview.json"
    get = url + json + keys

    # request and get the information stored at the link
    response = requests.get(get).json()

    return response
