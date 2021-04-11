"""CRUD opperations"""
from model import db, User, Book, UserBook, connect_to_db


def create_user(fname, lname, email, password, age, gender, city, country):
    """create and return new user"""

    user = User(fname = fname, lname= lname, email = email, password = password, age= age, gender= gender, city= city, country= country)
    db.session.add(user)
    db.session.commit()
    return user


def create_book(google_id, name, subject):
    """create and return new user"""

    book = Book(google_id = google_id, name= name, subject = subject)
    db.session.add(book)
    db.session.commit()
    return book


def save_user_books(user_id,google_id, review, favorite, suggest ):
    """save user and books relationship"""
    userbooks = UserBook(user_id= user_id, google_id = google_id, review= review, favorite=favorite, suggest= suggest)
    db.session.add(userbooks)
    db.session.commit()
    return userbooks




def get_allbooks():
    """return all books"""
    return Book.query.all()



def get_alluser():
    """return all user"""
    return User.query.all()

def get_user(userid):
    """get information of particular user"""

    return User.query.get(userid)

def userlogin(email,password):

    return User.query.filter( (User.email== email) &  (User.password ==password)).first()

# email =bmoore@yahoo.com 
# password=25Mz!Q(r+K
#



def get_books_of_user(user_id):
    """return books of particular user"""
    books = db.session.query(Book).join(UserBook).filter(UserBook.user_id==user_id).all()
    return books



    




if __name__ == '__main__':
    from server import app
    connect_to_db(app)


