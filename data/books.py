import json

import requests
import os
APIKEY = os.environ["APIKEY"]


def search_book_with_google_id(ids):
    """search book with google id and return books"""

    payload ={ "key" : APIKEY}
    books_api=[]
    for i in ids:
        url2 = "https://www.googleapis.com/books/v1/volumes/"+i[0]
        res=requests.get(url2, params = payload)
        books_api.append(res.json())
    books = []
    for book in books_api:
        google_id = book["id"]
        title = book['volumeInfo']['title']
        authors= [book['volumeInfo']['authors'] if 'authors'  in book['volumeInfo'].keys() else None]
        categoies = [book['volumeInfo']['categories'] if 'categories'  in book['volumeInfo'].keys() else None]
        imageLink =  book['volumeInfo']['imageLinks']
        books.append((google_id,title,authors,categoies,imageLink))


    return books



def get_books(keyword):
    """read 10 books"""
    url= "https://www.googleapis.com/books/v1/volumes"
    payload ={ "q":keyword,"key" : APIKEY}
    res=requests.get(url, params = payload)
    a = res.json()
    books = []
    for b in a['items']:
        id = b["id"]
        title = b['volumeInfo']['title']
        authors= [b['volumeInfo']['authors'] if 'authors'  in b['volumeInfo'].keys() else None]
        categoies = [b['volumeInfo']['categories'] if 'categories'  in b['volumeInfo'].keys() else None]
        imageLink =  b['volumeInfo']['imageLinks']
        books.append((id,title,authors,categoies,imageLink))


    return books



def get_book_arts():

    url= "https://www.googleapis.com/books/v1/volumes"
    payload ={ "q":"fiction" , "key" : APIKEY}
    res=requests.get(url, params = payload)

    a = res.json()
    books = []
    for b in a['items']:
        id = b["id"]
        title = b['volumeInfo']['title']
        authors= [b['volumeInfo']['authors'] if 'authors'  in b['volumeInfo'].keys() else None]
        categoies = [b['volumeInfo']['categories'] if 'categories'  in b['volumeInfo'].keys() else None]
        imageLink =  b['volumeInfo']['imageLinks']
        books.append((id,title,authors,categoies,imageLink))


    return books







    

def search(writer_name):
    
    "https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=yourAPIKey"
    
    url = "https://www.googleapis.com/books/v1/volumes"
    payload ={ "q":writer_name,  "key" : APIKEY}
    res = requests.get(url, params = payload)

    return res


# a=search("elif shafak")
# >>> a=a.json()
# >>> b=a["items"][0]
# >>> c=b["volummeInfo"]["authors"]
# >>> c=b["volumeInfo"]["authors"]
# >>> c
# ['Elif Shafak']
#a = search("elif shafak")


def search_books_in_order(keyword):
    url = "https://www.googleapis.com/books/v1/volumes"
    payload ={ "q":keyword, "orderBy":"newest", "key" : APIKEY}
    res = requests.get(url, params = payload)

    return res


def search_on_keyword():
    url ="https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=yourAPIKey"





#get book info and store in data base  


        
           






