"""CRUD opperations"""
from model import db, User, Book, UserBook, Friend, connect_to_db


def create_user(fname, img_url,email, password, age, gender,interest, city = None, country=None):
    """create and return new user"""

    user = User(fname = fname, img_url=img_url,email = email, password = password, age= age, gender= gender,interest=interest, city= city, country= country)
    db.session.add(user)
    db.session.commit()
    return user




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
    """checking user email and password and if it is confirmed with database return user"""
    return User.query.filter( (User.email== email) &  (User.password ==password)).first()
    

# email =martha33@elliott.com 
# password= (lU8lIbUZ+

#jamescuevas@butler.net
#+uM3RP82a6

def get_books_of_user(user_id):
    """return books of particular user"""
    books = db.session.query(Book).join(UserBook).filter(UserBook.user_id==user_id).all()
    return books




def get_favorite_suggest(user_id):
    """return user favorite and suggest books collection by getting google_id from database and 
    get books from google api in server """
    google_id=[]
    google_id.append(db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.favorite==True ) ).all())
    google_id.append(db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.suggest==True ) ).all())
    return google_id

def get_lend(user_id):
    """return user books which he can share by getting google_id from database and 
    get books from google api in server """
    google_id=db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.lend==True ) ).all()
    return google_id


def get_review_google_id(user_id):
    """return user favorite and suggest books collection by getting google_id from database and 
    get books from google api in server """
    google_id=db.session.query(Book.google_id).join(UserBook).filter((UserBook.user_id==user_id) &(UserBook.review != None ) ).all()
    review = db.session.query(UserBook.review).filter((UserBook.user_id==user_id) &(UserBook.review != None ) ).all()

    return (google_id,review)







def update_favorite_suggest(user_id,google_id,name,favorite,suggest,lend=None):
    """save user and books relationship"""
    userbook = UserBook.query.filter( (UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).first()
    if userbook:
        if favorite != None:
            userbook.favorite=favorite
        if suggest != None:
            userbook.suggest=suggest
        if lend != None:
            userbook.lend= lend
    else:
        book = Book.query.get(google_id)
        if book is None :
            book=create_book(google_id,name,subject=None)
        userbook = save_user_books(user_id, google_id,favorite,suggest)

    db.session.add(userbook)
    db.session.commit()
    return userbook


def save_review(user_id, google_id, name, review):
    """save review"""
    userbook = UserBook.query.filter( (UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).first()
    if userbook:
         userbook.review=review   
    else:
        book = Book.query.get(google_id)
        if book is None :
            book=create_book(google_id,name,subject=None)
        userbook = save_user_books(user_id, google_id,review=review)

    db.session.add(userbook)
    db.session.commit()
    return userbook

def delete_review(user_id,google_id):    
    userbook = UserBook.query.filter( (UserBook.user_id== user_id) &  (UserBook.google_id == google_id)).first()
    if userbook:
        db.session.delete(userbook)
        db.session.commit()
    return userbook





def update_friend_status(user_id,friend_user_id,status):

    friends = db.session.query(Friend).all()
    friend_return= None
    friend_user_id=int(friend_user_id)

    for friend in friends:
        if (friend.friend_user_id == user_id) and (friend.user_id == friend_user_id) or (friend.user_id == user_id) and (friend.friend_user_id == friend_user_id) :
            print(user_id,friend.user_id,friend.friend_user_id,"inside loop")
              
            if status == "accepted":
                friend.friend_status=status
                friend_return= friend
                db.session.add(friend_return)
                break
            else:
                friend_return="delete"
                db.session.delete(friend)
                break
          
    if friend_return is None:
        friend_return= Friend(user_id=user_id,friend_user_id=friend_user_id, friend_status=status)
        db.session.add(friend_return)
    
    db.session.commit()
    return friend_return





def get_requested_friend(userid):
    """return friend requests of particular user"""
    friends = db.session.query(Friend.user_id, Friend.friend_user_id,Friend.friend_status).filter((Friend.friend_user_id==userid) & (Friend.friend_status=="requested")).all()
    users_friends = []
    for user, friend, friend_status in friends:  
        users_friends.append(db.session.query(User).filter((User.user_id==user) & (User.user_id != userid)).first())
        
    return users_friends



def get_friend(userid):
    """return all friends of particular user"""
    friends = db.session.query(Friend.user_id, Friend.friend_user_id,Friend.friend_status).filter(((Friend.user_id==userid) | (Friend.friend_user_id==userid)) & (Friend.friend_status=="accepted")).all()
    users_friends = []
    for user, friend, friend_status in friends: 
        users_friends.append(User.query.filter(((User.user_id == friend) | (User.user_id==user)) & (User.user_id != userid)).first())

    return users_friends
    #email : mhopkins@goodwin.org
    #password: 4S9P*RvvP$'


#use these function to seed database with random data for developemt purpose

def create_book(google_id, name, subject=None):
    """create and return new user"""

    book = Book(google_id = google_id, name= name, subject = subject)
    db.session.add(book)
    db.session.commit()
    return book


def save_user_books(user_id,google_id, favorite=False, suggest = False , review=None,lend=False):
    """save user and books relationship"""
    userbook = UserBook(user_id= user_id, google_id = google_id, review= review, favorite=favorite, suggest=suggest)
    db.session.add(userbook)
    db.session.commit()
    return userbook


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


