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


def save_user_books(user_id,google_id, review=None, favorite=False, suggest = False ):
    """save user and books relationship"""
    
    userbook = UserBook(user_id= user_id, google_id = google_id, review= review, favorite=favorite, suggest=suggest)
    db.session.add(userbook)
    db.session.commit()
    return userbook

    #save_user_books(2,YYwaEAAAQBAJ)


def update_userbook_favorite(user_id,google_id,name, favorite):
    """save user and books relationship"""
    userbook = UserBook.query.filter( (UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).first()
    if userbook:
        userbook.favorite=favorite
        #db.session.query(UserBook).filter((UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).update({'favorite':favorite})
    else:
        book = Book.query.get(google_id)
        if book:
            userbook = save_user_books(user_id, google_id,None,favorite)
        else:
            book=create_book(google_id,name,subject=None)
            userbook = save_user_books(user_id, google_id,None,favorite)

    db.session.add(userbook)
    db.session.commit()
    return userbook


def update_userbook_suggest(user_id,google_id, name, suggest):
    """update user and books """
    userbook = UserBook.query.filter( (UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).first()
    if userbook:
        userbook.suggest=suggest
    else:
        book = Book.query.get(google_id)
        if book:
            userbook = save_user_books(user_id, google_id,None,suggest)
        else:
            book=create_book(google_id,name,subject=None)
            userbook = save_user_books(user_id, google_id,None,False,suggest)
    db.session.add(userbook)
    db.session.commit()
    return userbook






def get_allbooks():
    """return all books"""
    return Book.query.all()



def get_alluser():
    """return all user"""
    return User.query.all()

def get_user(userid):
    """get information of particular user"""

    return User.query.get(userid)

def get_userbook():
    return UserBook.query.all()

def userlogin(email,password):

    return User.query.filter( (User.email== email) &  (User.password ==password)).first()

# email =bmoore@yahoo.com 
# password=25Mz!Q(r+K
#

def get_books_of_user(user_id):
    """return books of particular user"""
    books = db.session.query(Book).join(UserBook).filter(UserBook.user_id==user_id).all()
    return books


def get_favorite(user_id):
    google_id=[]
    google_id.append(db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.favorite==True ) ).all())

    google_id.append(db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.suggest==True ) ).all())
   

    return google_id





if __name__ == '__main__':
    from server import app
    connect_to_db(app)


