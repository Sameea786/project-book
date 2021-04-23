from unittest import TestCase
from model import connect_to_db,db
from server import app
from flask import session
import crud
import seed

# testing routes witout login
class TestBooks(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['Testing'] = True
        connect_to_db(app)

    def test_get_books_list(self):
        """test index page"""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200) 
        self.assertIn(b"book-info",result.data)


    def test_login_page(self):
        """test log in page load"""
        result = self.client.get("/login")
        self.assertEqual(result.status_code,200)
        self.assertIn(b"form-signin",result.data)

    def test_invalid_user(self):
        result = self.client.post("/processlogin",
                                  data={"email": "bmoore@yahoo.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"You need to sign up", result.data)



    def test_login(self):
        """Test login if user exist ."""

        result = self.client.post("/processlogin",
                                  data={"email": "bmoore@yahoo.com", "password": "25Mz!Q(r+K"},
                                  follow_redirects=True)
        self.assertIn(b"Log out", result.data)

    
    def test_signup(self):
        result =self.client.get('/signup')
        self.assertEqual(result.status_code,200)
        self.assertIn(b"form-signup",result.data)


#test cases where user need to log in

class TestBooksLogIn(TestCase):

    def setUp(self):
        
        app.config['Testing'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        connect_to_db(app)

        with self.client as c:
            with c.session_transaction() as session:
                session["id"]  = 1


    def test_user_profile(self):
        """testing user profile when he is already loged in"""
        result = self.client.get("/userprofile")
        self.assertIn(b"Friend Requests",result.data)

    
    def test_signup(self):
        """test if person is login but try to signup again using url"""
        result = self.client.get("/signup", follow_redirects=True)
        self.assertEqual(result.status_code,200)
        self.assertIn(b"Search", result.data)

    
    def  test_favouriteSuggest(self):
        """add book in  user favorite collection who is already logged in"""
        
        result = self.client.post("/favoriteSuggest",data={'google_id':'5Zpq0Rmm7hQC','status':'true'})
        self.assertIn(b"favorite collection",result.data)

    
    def test_show_all_users(self):
        """show all user to logged in user, if he want, he can send friend request"""

        result = self.client.get("/users")
        self.assertIn(b"Add Friend",result.data)

    
    def test_manage_friend_request(self):
        """send friend request and check status if it get changed"""

        result = self.client.post("/manageFriend",data={'user_id':5 ,'status':'requested'})
        self.assertIn(b"requested",result.data)


class  TestsDatabase(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['Testing']= True
        connect_to_db(app,"postgresql:///userbookstestdb")

        #creating tables and seeding testing database
        db.create_all()
       
        seed.store_books_in_database()
        seed.store_user_in_database()
        users=crud.get_alluser()
        books=crud.get_allbooks()
        seed.store_userbooks_in_database(users,books)


    def tearDown(self):
        """drop db and remove session after connection"""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    
    def test_update_friend_status(self):
        """test update friend status by sending requests, accepts, rejects as status"""

        result = crud.update_friend_status(1,2,"requested")
        self.assertIn(result.friend_status,"requested")

    # def test_update_friend_status_acepted(self):
    #     """test update friend status by sending requests, accepts, rejects as status"""

    #     result = crud.update_friend_status(2,1,"accepted")
    #     self.assertIn(result.friend_status,"accepted")


    def test_get_friend(self):
        """test crud get_friend function and it will retusn list of friends """

        result = crud.get_friend(1)
        self.assertEqual(type(result),list)
        #self.assertIn(result[0].status,"accepted")



if __name__ == "__main__":

    import unittest
    unittest.main()


