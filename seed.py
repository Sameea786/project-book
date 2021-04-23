from data.books import get_books
import crud
import model
import server
import os
import random
from faker import Faker


#os.system('dropdb usersbooks')
#os.system('createdb usersbooks')
model.connect_to_db(server.app)
model.db.create_all()

def store_books_in_database():
    a = get_books("cooking")
    id_record= []
   
    for b in a:
        id=b[0]
        title = b[1]
        crud.create_book(id ,title,"None")
  

def store_user_in_database():
    faker = Faker()
    default_gender =["Male","Female"]
    for i in range(20):
        email = faker.email()
        password= faker.password()
        name= faker.name()
        fname=name.split()[0]
        lname = name.split()[1]
        age = random.choice(range(15,50))
        gender = random.choice(default_gender)
        city = faker.city()
        country = faker.country()
        crud.create_user(fname, lname,email, password, age, gender, city, country)



def store_userbooks_in_database(users, books):
    default =[True,False]
    faker = Faker()
    for i in range(10):
        user = random.choice(users)
        google = random.choice(books)
        favorite = random.choice(default)
        suggest = random.choice(default)
        review = faker.text()
        crud.save_user_books(user.user_id,google.google_id,favorite,suggest,review)



def make_user_id_and_book_id():
    """make list of user id's and google id's"""

    userid_list= []
    bookid_list= []

    for user in crud.get_alluser():
        userid_list.append(user.user_id)
    
    for book in crud.get_allbooks():
        bookid_list.append(book.google_id)

    return userid_list, bookid_list



    






