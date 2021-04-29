"""server for book website"""

from flask import (Flask , render_template, request, flash, session, redirect,jsonify)
from model import connect_to_db
import crud
from data.books import get_books,search_book_with_google_id

from jinja2 import StrictUndefined
import cloudinary.uploader
import os

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_KEY_SECRET = os.environ['CLOUDINARY_SECRET']



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
        name = user.fname
        img_url=user.img_url
        google_id = crud.get_favorite_suggest(session['id']) # this function is returning all googlgle key which have 
        return render_template("userProfile.html", name=name, email=user.email, img_url=img_url)
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

    fname = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    gender= request.form.get("gender")
    user_image = request.files['userimage']
    interest = request.form.get("interest")
    print(CLOUDINARY_KEY_SECRET)
    result = cloudinary.uploader.upload(user_image,api_key=CLOUDINARY_KEY,api_secret=CLOUDINARY_KEY_SECRET,
    cloud_name="dj4hb9gek")
    img_url=result['secure_url']
    user=crud.create_user(fname,img_url,email,password,age,gender,interest)
    return redirect("/")
    

@app.route('/favoriteSuggest',methods=["POST"])
def favorite_suggest():
    """Add or remove book from user favorite and suggestion collection 
    by getting check box through javascript"""
    if session.get("id",None):
        name=request.form.get("name")
        google_id = request.form.get("google_id")
        if "suggest" in google_id:
            google_id = google_id.split('-')[1]
            status,message = [(True,"This book has been add to your suggest collection") if request.form.get("status") == "true" else (False,"This book removed from your suggest collection")][0]
            userbook=crud.update_favorite_suggest(session["id"],google_id,name,None,status)
        elif "lend" in google_id:
            google_id = google_id.split('-')[1]
            status,message = [(True,"Lend") if request.form.get("status") == "true" else (False,"Not available for Lend")][0]
            userbook=crud.update_favorite_suggest(session["id"],google_id,name,None,None,status)
        else:
            status,message = [(True,"This book has been add to your favorite collection") if request.form.get("status") == "true" else (False,"This book removed from your favorite collection")][0]
            userbook=crud.update_favorite_suggest(session["id"],google_id,name, status,None)
        return jsonify({'message':message})
    else:
        return jsonify({'message':'You need to sign up'})



@app.route('/addreview',methods = ["POST"])
def add_review():
    """add review of book in database"""

    if session.get("id",None):
        name = request.form.get("name")
        google_id = request.form.get("google_id")
        review = request.form.get("value")
        userbook=crud.save_review(session["id"],google_id,name,review)
        print(userbook)
        return jsonify({"message":"Your review is added"})
    else:
        return jsonify({"message":"You need to sign up"})
    

@app.route('/deletereview', methods= ["POST"])
def delete_review():

    google_id = request.form.get("google_id")
    print(google_id)
    userbook = crud.delete_review(session["id"], google_id)
    return jsonify({"message":"You delete your review"})

    




@app.route("/users")
def show_all_users():
    """if user is logged in show them all user who is not their friend otherwise redirect to index.html"""
    if session.get("id",None):
        allusers=crud.get_alluser()
        friends=crud.get_friend(session['id'])
        user = [crud.get_user(session['id'])]  #getting user object convert it to list for set subtration
        users= list(set(allusers)-set(friends)-set(user))
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
        print(type(session['id']))
        friend=crud.update_friend_status(session['id'],friend_id,status)
        if friend:
            print("loop delete")
            return jsonify({'message': status})
            
        else:
            print("issue")
            return jsonify({'message':'Issue with request'})
    else:
        return redirect("/")



@app.route("/review")
def get_review():
    
    google_id_with_review = crud.get_review_google_id(session['id'])
    books=search_book_with_google_id(google_id_with_review[0])
    return render_template("userreview.html",fav_books=books,reviews =  google_id_with_review[1],zip=zip)


@app.route("/favorite")
def get_favorite():
    
    friend_id= request.args.get("friend_id")
    # if friend_id:
    #     google_id = crud.get_favorite_suggest(friend_id) # this function is returning all googlgle key which have 
    #     fav_books = search_book_with_google_id(google_id[0])
    # else:
    print("favorite")
    google_id = crud.get_favorite_suggest(session['id']) # this function is returning all googlgle key which have 
    fav_books = search_book_with_google_id(google_id[0])
    return render_template("favoritebook.html",fav_books=fav_books)

@app.route("/suggest")
def get_suggest():

    google_id = crud.get_favorite_suggest(session['id']) # this function is returning all googlgle key which have 
    suggest_books = search_book_with_google_id(google_id[1])
    print("suggest")
    return render_template("suggestbook.html",suggest_books=suggest_books)

@app.route("/requestfriend")
def get_requested_friend():

    requested_friend=crud.get_requested_friend(session['id'])
    return render_template("requestfriend.html", friend_requests=requested_friend)

@app.route("/friends")
def get_friends():

    friends= crud.get_friend(session['id'])
    #logic_for_friend()
    return render_template("friends.html", friends=friends)

def logic_for_friend():
    friends= crud.get_friend(session['id'])
    friend_list=[]
    for friend in friends:
        google_id = crud.get_favorite_suggest(friend.user_id) # this function is returning all googlgle key which have 
        fav_books = search_book_with_google_id(google_id[0])
        suggest_books = search_book_with_google_id(google_id[1])
        
        friend_list.append([friend,fav_books,suggest_books])
    print(friend_list)




@app.route("/sharebooks")
def get_sharebooks():
    google_id = crud.get_lend(session['id'])
    books=search_book_with_google_id(google_id)
    return render_template("sharebook.html", books=books)




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)