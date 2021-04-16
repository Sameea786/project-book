"""server for book website"""

from flask import (Flask , render_template, request, flash, session, redirect,jsonify)
from model import connect_to_db
import crud
from data.books import get_book_arts,get_books,search_book_with_google_id


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
    
    if 'id' in session: 
        return render_template("index.html",books=BOOKs)
    else:
        return render_template("index.html",books=BOOKs)




@app.route('/login')
def login():
    """check if user is already log in then send on home page otherwise send him on login page"""
    
    print("*"*10,session.get("id",False))
    if session.get("id") is None:
        return render_template("login.html" )
    else:
        return redirect("/")



@app.route('/processlogin', methods=["POST"])
def process_login():
    """check user email and password with database and handle log in"""

    email= request.form.get('email')
    password= request.form.get('password')
    user=crud.userlogin(email,password)
    if user:
        session["id"] =user.user_id
        return redirect("/")
    else:
        return "You need to sign up"



@app.route('/logout')
def process_logout():
    """in this function user will be logout by assigning session None"""
    session["id"] =None
    print("*"*10,session["id"])
    return redirect("/")



@app.route('/addfavorite/<string:google_id>/<string:name>')
def add_favorite(google_id,name):
    """this function will add book in user favorite books"""
    
    if session.get("id",None):
        crud.update_userbook_favorite(session["id"],google_id,name, True)
        return jsonify({'message':'This book added to your favorite'})
    else:
        return jsonify({'message':'You need to sign up'})



@app.route('/addsuggest/<string:google_id>/<string:name>')
def add_suggest(google_id,name):
    """this function will add book in user suggestion"""
    
    if session.get("id",None):
        google_id = google_id.split('-')[1]
        crud.update_userbook_suggest(session["id"],google_id,name, True)
        return jsonify({'message':'You suggested this book'})
    else:
        return jsonify({'message':'You need to sign up'})



@app.route('/search')
def search_book():
    """search book"""
    search_keyword=request.args.get("search")
    books=get_books(search_keyword)
    return  render_template("index.html", books= books)



@app.route('/userprofile')
def user_profile():
    """user profile and return his favorite and suggested book """
    if session.get("id") is not None:
        user=crud.get_user(session['id'])
        name = user.fname+" "+user.lname
        google_id = crud.get_favorite(session['id'])
        fav_books = search_book_with_google_id(google_id[0])
        suggest_books = search_book_with_google_id(google_id[1])
        return render_template("userProfile.html",fav_books=fav_books,suggest_books=suggest_books, name=name, email=user.email)
    else:
       return redirect("/" )


@app.route('/signup')
def sign_up():
    
    if session.get("id") is None:
        return render_template("signup.html")
    else:
        return redirect("/login")



@app.route('/processSignup', methods=["POST"])
def process_signup():

    fname,lname = request.form.get("name").split()
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    gender= request.form.get("gender")
    user=crud.create_user(fname,lname,email,password,age,gender)
    print(user)
    return redirect("/")
    





    if session.get("id") is None:
        return render_template("signup.html")
    else:
        return redirect("/login")






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)