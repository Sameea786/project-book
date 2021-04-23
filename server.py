"""server for book website"""

from flask import (Flask , render_template, request, flash, session, redirect,jsonify)
from model import connect_to_db
import crud
from data.books import get_books,search_book_with_google_id

from jinja2 import StrictUndefined



app = Flask(__name__)
#app.secrete_key = "dev"
app.secret_key = 'this-should-be-something-unguessable'
app.jinja_env.undefined = StrictUndefined
ID= 1
BOOKs=get_books('fiction')

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
    return redirect("/")


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
        google_id = crud.get_favorite_suggest(session['id'])
        fav_books = search_book_with_google_id(google_id[0])
        suggest_books = search_book_with_google_id(google_id[1])
        requested_friend=crud.get_requested_friend(session['id'])
        friends= crud.get_friend(session['id'])
        return render_template("userProfile.html",fav_books=fav_books,suggest_books=suggest_books, name=name, email=user.email, friend_requests=requested_friend,friends=friends)
    else:
       return redirect("/" )


@app.route('/signup')
def sign_up():
    if session.get("id") is None:
        return render_template("signup.html")    
    else:
        return redirect("/")



@app.route('/processSignup', methods=["POST"])
def process_signup():
    """this function will save user get information from sign up 
    form, save in database and return him to index page"""

    fname,lname = request.form.get("name").split()
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    gender= request.form.get("gender")
    user=crud.create_user(fname,lname,email,password,age,gender)
    return redirect("/")
    

@app.route('/favoriteSuggest',methods=["POST"])
def favorite_suggest():
    """Add or remove book from user favorite and suggestion collection 
    by getting check box through javascript"""
    if session.get("id",None):
        name=request.form.get("name")
        google_id = request.form.get("google_id")
        if 'suggest' in google_id:
            google_id = google_id.split('-')[1]
            status,message = [(True,"This book has been add to your suggest collection") if request.form.get("status") == "true" else (False,"This book removed from your suggest collection")][0]
            userbook=crud.update_favorite_suggest(session["id"],google_id,name,None,status)
        else:
            status,message = [(True,"This book has been add to your favorite collection") if request.form.get("status") == "true" else (False,"This book removed from your favorite collection")][0]
            userbook=crud.update_favorite_suggest(session["id"],google_id,name, status,None)
        return jsonify({'message':message})
    else:
        return jsonify({'message':'You need to sign up'})


@app.route("/users")
def show_all_users():
    """if user is logged in show them all user otherwise redirect to index.html"""
    if session.get("id",None):
        users=crud.get_alluser()
        friends=crud.get_friend(session['id'])
        use= set(users)
        return render_template("users.html",users=users)
    else:
        return redirect("/")



@app.route("/manageFriend",methods=["POST"])
def manage_friend():
    """if user is logged in managing user friend request(requested, accepted, rejected)
    and creating and updating database accoriding to request else redireect to index.html """

    if session.get("id",None):
        friend_id=request.form.get("user_id")
        status=request.form.get("status")
        print(status,session['id'],friend_id)
        friend=crud.update_friend_status(session['id'],friend_id,status)
        if friend:
            return jsonify({'message': status})
        else:
            return jsonify({'message':'Issue with request'})
    else:
        return redirect("/")
    



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)