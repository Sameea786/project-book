"""Models for Books"""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    """User info"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    email = db.Column(db.String(50), unique= True, nullable = False)
    password = db.Column(db.String(15),  nullable= False)
    fname = db.Column(db.String(30), nullable = False)
    lname = db.Column(db.String(30))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    city = db.Column(db.String(100))
    country = db.Column(db.String(50))
    user_friends = db.relationship('User', secondary='friends', primaryjoin=('User.user_id== Friend.user_id'),secondaryjoin = ('User.user_id== Friend.friend_user_id'))
   #relationship = db.relationship('UserBook')

    def __repr__(self):
        return f'<User fname={self.fname} lname = {self.lname}, email ={self.email} >'


class Book(db.Model):
    """Books Info"""

    __tablename__= 'books'

    google_id = db.Column(db.String, primary_key= True)
    name = db.Column(db.String(100), nullable= False)
    subject = db.Column(db.String(100))


    #relationship = db.relationship('UserBook')

    def __repr__(self):
        return f'<Book name={self.name}, google_id = {self.google_id}, >'


class UserBook(db.Model):
    """user and books relationship"""

    __tablename__ = 'users_books'

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False )
    google_id = db.Column(db.String, db.ForeignKey('books.google_id'), nullable= False)
    review = db.Column(db.String(300))
    favorite = db.Column(db.Boolean, default=False)
    suggest = db.Column(db.Boolean, default= False)
    user_relationship = db.relationship('User', backref='UserBook')
    book_relationsip = db.relationship('Book', backref='UserBook')
    
    def __repr__(self):
        return f'<UserBook user_id={self.user_id}, google_id= {self.google_id}>'

    
class Friend(db.Model):
    """a user's friend"""
    __tablename__ = 'friends'

    id = db.Column(db.Integer, 
                    autoincrement=True,
                    primary_key=True)
    friend_status = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    friend_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable = False)
   


    def __repr__(self):
        return f'<Friend user_id = {self.user_id}, friend_user_id= {self.friend_user_id}>'



def connect_to_db(app,db_uri="postgresql:///usersbooks"):
    """Connect the database to our Flask app."""
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")


if __name__ == "__main__":

    from flask import Flask
    app = Flask(__name__)
    #from server import app
    connect_to_db(app)






