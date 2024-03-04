# NYTimes Developer (Books API)
# Sarah Pham

import requests
# make sure to manually install mysql.connector package
import mysql.connector
from mysql.connector import errorcode

# Setting up string for requesting info
access_key = "qgSd60mPz5XAxiNttMJroiDMmKWMmN1B"
secret_key = "vzwESl6P5JqBwtBZ"  # not sure if it's needed but putting heere
keys = "?api-key=" + access_key
url = "https://api.nytimes.com/svc/books/v3"
json = "/lists/full-overview.json"
get = url + json + keys

# make sure the URL printed out is correct
# print(get)

# request and get the information stored at the link
response = requests.get(get)

# if returns 200, the information was successfully retrieved
# if returns 403, access was denied (lack of authorization)
print(response)

# the actual data, in dict format
data = response.json()
# print(data['num_results'])          # number of books in the list
# print(data['results']['books'])     # the actual list of books
# print(data['results']['books'][0]['title'])

# connecting to database inside try catch in case of errors
#   try catch taken from:
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
try:
    mydb = mysql.connector.connect (
        # fill accordingly to your api
        host='127.0.0.1',
        user='root',
        password=''#,
        # database='books'  # create a database called 'books' before using this
        # using 'test' for now to make sure it works
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    # print('\nyou did it')
    mycursor = mydb.cursor()

    # creating the database
    # note: make sure that a database with this name
    mycursor.execute("CREATE DATABASE books")
    # # use newly created database
    mycursor.execute("USE books")

    # creating the table
    mycursor.execute("""CREATE TABLE bestsellers (
    id INT AUTO_INCREMENT PRIMARY KEY,
     title VARCHAR(255),
     author VARCHAR(255),
     publisher VARCHAR(255),
     isbn_13 VARCHAR(13),
     isbn_10 VARCHAR(10) )""")

    # i'm looking online for how to store long text and it doesn't seem viable
    # so maybe we should stick to finding different publishers and other links finding it
    # descriptions doesn't seem viable

    # testing out inserting one value
    # try:
    #     # testing for 1 value first
    #     first_book = data['results']['books'][0]
    #     sql = """INSERT INTO hardcover_fiction (title, author, publisher, isbn_13, isbn_10)
    #      VALUES (%s, %s, %s, %s, %s)"""
    #     val = (first_book['title'], first_book['author'], first_book['publisher'],
    #            first_book['primary_isbn13'], first_book['primary_isbn10'] )
    #     mycursor.execute(sql, val)
    #
    #     mydb.commit()
    # except:
    #     print('failed')
    # else:
    #     print('yay')

    # from the list of bestsellers
    for list_dict in data['results']['lists']:
        # getting the books for each list into the database
        for book_dict in list_dict['books']:
            title = book_dict['title']
            author = book_dict['author']
            publisher = book_dict['publisher']
            isbn_13 = book_dict['primary_isbn13']
            isbn_10 = book_dict['primary_isbn10']

            # set up sql statement
            sql = """INSERT INTO bestsellers (title, author, publisher, isbn_13, isbn_10)
             VALUES (%s, %s, %s, %s, %s)"""
            val = (title, author, publisher, isbn_13, isbn_10)

            # execute sql statement + committing to database
            mycursor.execute(sql, val)
            mydb.commit()

            # break for testing out a few
            # break

    print("records inserted")
    mydb.close()

# ensure that it's always done
finally:
    # make sure the running of the code got here
    print('\nEntire file was executed')
