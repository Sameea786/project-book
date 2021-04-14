"""server for book website"""

from flask import (Flask , render_template, request, flash, session, redirect,jsonify)
from model import connect_to_db
import crud
from data.books import get_book_arts

#import crud
from jinja2 import StrictUndefined



app = Flask(__name__)
#app.secrete_key = "dev"
app.secret_key = 'this-should-be-something-unguessable'
app.jinja_env.undefined = StrictUndefined
ID= 1
BOOKs=get_book_arts()
@app.route('/')
def homepage():
    """View homepage."""
   
    print("#"*10, session.get("id",None))
    ID=None
    
    if 'id' in session:
        print("#"*10, "logout i")
        return render_template("index.html",books=BOOKs,session_id=session['id'])
    else:
        print("*"*10, "login o")
        return render_template("index.html",books=BOOKs,session_id=None)
        


@app.route('/login')
def login():
    
    print("*"*10,session.get("id",False))
    if session.get("id") is None:
        
        return render_template("login.html", session_id=None )
    else:
        return render_template("index.html",books=BOOKs,session_id=session['id'])


@app.route('/processlogin', methods=["POST"])
def process_login():

    email= request.form.get('email')
    password= request.form.get('password')
   
    user=crud.userlogin(email,password)
    if user:
        session["id"] =user.user_id
        print("*"*10,user.user_id) 
        return render_template("index.html",books=BOOKs,session_id=session['id'])
    else:
        return "You need to sign up"


@app.route('/logout')
def process_logout():
    session["id"] =None
    print("@"*10,session["id"])
    return render_template("index.html", books= BOOKs,session_id=session['id'])



@app.route('/addfavorite/<string:google_id>/<string:name>')
def add_favorite(google_id,name):
    
    if session.get("id",None):
        crud.update_userbook_favorite(session["id"],google_id,name, True)
        return jsonify({'message':'This book added to your favorite'})
    else:
        return jsonify({'message':'You need to sign up'})



@app.route('/addsuggest/<string:google_id>/<string:name>')
def add_suggest(google_id,name):
    
    if session.get("id",None):
        google_id = google_id.split('-')[1]
        crud.update_userbook_suggest(session["id"],google_id,name, True)
        return jsonify({'message':'You suggested this book'})
    else:
        print("*"*10)
        return jsonify({'message':'You need to sign up'})








if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)