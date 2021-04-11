"""server for book website"""

from flask import (Flask , render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from data.books import get_book_arts

#import crud
from jinja2 import StrictUndefined



app = Flask(__name__)
#app.secrete_key = "dev"
app.secret_key = 'this-should-be-something-unguessable'
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""
    books=get_book_arts()

    return render_template("index.html",books=books)

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/processlogin', methods=["POST"])
def process_login():
    email= request.form.get('email')
    password= request.form.get('password')

    user=crud.userlogin(email,password)
    if user:
        session["id"] =user.user_id
        return render_template("userProfile.html")
    else:
        return "You need to sign up"


@app.route('/processlogout')
def process_logout():
    session["id"] ={}
    return render_template("index.html")



    




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)