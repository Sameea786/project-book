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
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    
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


def connect_to_db(app):
    """Connect the database to our Flask app."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///usersbooks"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)






