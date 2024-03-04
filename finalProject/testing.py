from utils import *

import requests
import json

import mysql.connector
from mysql.connector import errorcode

if __name__ == '__main__':
    # removed param for connect so that below sql statements work
    mydb, mycursor = connect()

    mycursor.execute("DROP DATABASE IF EXISTS books")
    mycursor.execute("CREATE DATABASE books")
    mycursor.execute("USE books")

    # next three tables prevent repetition of info + transitive functional dependencies
    # for example, an author's name can change
    mycursor.execute("""CREATE TABLE publishers (
        publisher_id INT AUTO_INCREMENT PRIMARY KEY,
        publisher VARCHAR(255) )""")

    # created a table separate for descriptions since they might be very long
    # would make retrieving from books table harder if descriptions stored there
    mycursor.execute("""CREATE TABLE descriptions (
        description_id INT AUTO_INCREMENT PRIMARY KEY, 
        description TEXT DEFAULT NULL )""")

    mycursor.execute("""CREATE TABLE books (
                book_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                isbn_13 VARCHAR(13),
                isbn_10 VARCHAR(10),
                publisher_id INT, 
                description_id INT, 
                FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id), 
                FOREIGN KEY(description_id) REFERENCES descriptions(description_id) )""")

    # created in this order due to foreign keys of the previous tables
    # these foreign keys prevent invalid data from being inserted

    # author's name separated into first and last name for more in-depth searching
    # would've made author_id a foreign key in books, but there can be multiple authors
    mycursor.execute("""CREATE TABLE authors (
            author_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255), 
            last_name VARCHAR(255), 
            book_id INT, 
            FOREIGN KEY(book_id) REFERENCES books(book_id) )""")

    # some books have SEVERAL genres, making it impossible to have foreign keys
    # for genres (some have 5+); it's one book to many genres
    # for searching a specific genre, it would have to be a string match and then
    # looking at the corresponding book_ids
    mycursor.execute("""CREATE TABLE genres (
            genre_id INT AUTO_INCREMENT PRIMARY KEY,
            genre VARCHAR(40), 
            book_id INT, 
            FOREIGN KEY(book_id) REFERENCES books(book_id) )""")

    # ny times is several lists of bestsellers
    ny_times = get_nytimes()['results']['books']

    # to ensure ids match for genre, description, author
    id = 1

    # getting books for each list into the database
    for book_dict in ny_times:
        # retrieval of information
        title = book_dict['title']
        authors = book_dict['author'].split(' and ')
        publisher = book_dict['publisher']
        isbn_13 = book_dict['primary_isbn13']
        isbn_10 = book_dict['primary_isbn10']
        print(title)
        print(authors)
        print(isbn_13)

        openlib = get_openlibrary(isbn_13)
        googlebooks = get_googlebooks(isbn_13)
        print(openlib)

        desc = googlebooks['description']
        genres = openlib['subject']

        # inserting the first few tables first before books table
        # checking if the publisher is already in the table
        # there's only one publisher per isbn, but one publisher can publish many books
        publisher_select = """SELECT publisher_id FROM publishers
                                WHERE publisher = %s"""
        publisher_tuple = (publisher,)
        mycursor.execute(publisher_select, publisher_tuple)

        row = mycursor.fetchone()
        # saving publisher_id to add to books table when the time comes
        publisher_id = 0
        if row is not None:
            publisher_id = row[0]
        else:
            # if no entry exists for that publisher, create it
            publisher_insert = """INSERT INTO publishers (publisher)
                                    VALUES (%s)"""
            mycursor.execute(publisher_insert, publisher_tuple)

            # now get the publisher id noww that it exists
            mycursor.execute(publisher_select, publisher_tuple)
            publisher_id = mycursor.fetchone()[0]

        # print(publisher_id)

        # now insert the description into its table
        # the desc_id matches the book one to one (description can be empty)
        desc_insert = """INSERT INTO descriptions (description)
                            VALUES (%s)"""
        desc_tuple = (desc,)
        mycursor.execute(desc_insert, desc_tuple)

        # now create the entry in the books table
        books_insert = """INSERT INTO books (title, isbn_13, isbn_10, publisher_id, description_id)
                            VALUES(%s, %s, %s, %s, %s)"""
        # id since description_id is the same
        books_tuple = (title, isbn_13, isbn_10, publisher_id, id)
        mycursor.execute(books_insert, books_tuple)

        # done last due to foreign key for books
        for genre in genres:
            if "nyt" in genre:
                continue

            genre_insert = """INSERT INTO genres (genre, book_id)
                                VALUES (%s, %s)"""
            genre_vals = (genre, id)
            mycursor.execute(genre_insert, genre_vals)

        # all authors in format first last name
        for author in authors:
            # splitting the author up by first and last name
            author = author.split(' ')
            first_name = author[0]
            last_name = author[1]

            author_insert = """INSERT INTO authors (first_name, last_name, book_id)
                                VALUES (%s, %s, %s)"""
            author_tuple = (first_name, last_name, id)
            mycursor.execute(author_insert, author_tuple)

        # increment so that way description_id changes
        id += 1
        mydb.commit()
        break

    mydb.close()