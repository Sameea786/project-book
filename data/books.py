import json

import requests
import os
APIKEY = os.environ["APIKEY"]


def search_book_with_google_id(id):
    
    url2 = "https://www.googleapis.com/books/v1/volumes/"+id
    payload ={ "key" : APIKEY}
    res=requests.get(url2, params = payload)
    return res.json()



def get_books():
    """read 10 books"""
    url= "https://www.googleapis.com/books/v1/volumes"
    payload ={ "q":"shafak","key" : APIKEY}
    res=requests.get(url, params = payload)

    
    json = res.json()

    return json

def get_book_arts():

    url= "https://www.googleapis.com/books/v1/volumes"
    payload ={ "q":"fiction" , "key" : APIKEY}
    res=requests.get(url, params = payload)

    a = res.json()
    books = []
    for b in a['items']:
        title = b['volumeInfo']['title']
        authors= [b['volumeInfo']['authors'] if 'authors'  in b['volumeInfo'].keys() else None]
        categoies = [b['volumeInfo']['categories'] if 'categories'  in b['volumeInfo'].keys() else None]
        imageLink =  b['volumeInfo']['imageLinks']
        books.append((title,authors,categoies,imageLink))


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


        
           






