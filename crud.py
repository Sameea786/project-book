"""CRUD opperations"""
from model import db, User, Book, UserBook, connect_to_db


def create_user(fname, lname, email, password, age, gender, city = None, country=None):
    """create and return new user"""

    user = User(fname = fname, lname= lname, email = email, password = password, age= age, gender= gender, city= city, country= country)
    db.session.add(user)
    db.session.commit()
    return user


def create_book(google_id, name, subject=None):
    """create and return new user"""

    book = Book(google_id = google_id, name= name, subject = subject)
    db.session.add(book)
    db.session.commit()
    return book


def save_user_books(user_id,google_id, favorite=False, suggest = False , review=None):
    """save user and books relationship"""
    
    userbook = UserBook(user_id= user_id, google_id = google_id, review= review, favorite=favorite, suggest=suggest)
    db.session.add(userbook)
    db.session.commit()
    return userbook

#save_user_books(2,YYwaEAAAQBAJ)


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


def get_favorite_suggest(user_id):
    google_id=[]
    google_id.append(db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.favorite==True ) ).all())
    google_id.append(db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.suggest==True ) ).all())
    return google_id







def update_favorite_suggest(user_id,google_id,name,favorite,suggest):
    """save user and books relationship"""
    userbook = UserBook.query.filter( (UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).first()
    if userbook:
        if favorite != None:
            userbook.favorite=favorite
        if suggest != None:
            userbook.suggest=suggest
    else:
        book = Book.query.get(google_id)
        if book is None :
            book=create_book(google_id,name,subject=None)
        userbook = save_user_books(user_id, google_id,favorite,suggest)

    db.session.add(userbook)
    db.session.commit()
    return userbook





if __name__ == '__main__':
    from server import app
    connect_to_db(app)


