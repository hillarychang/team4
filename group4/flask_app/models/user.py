# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash

from flask_app.models import travelinfo

from flask_app import app



from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)     

import re	# the regex module

class User: # model the class after the user table from the database
    
    db='travel_log' #database (in mySQL workbench)

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.trips=[] # one to many



    @classmethod
    def get_user_with_logs( cls , data ):
        query = """
        SELECT * FROM user 
        LEFT JOIN trips ON trips.user_id = user.id 
        WHERE user.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db( query , data )
        # results will be a list of user objects with the log attached to each row. 
        
        if len(results)<1:
            return

        user = cls( results[0] )
        for row_from_db in results:
            # Now parse the post data to make instances of logs and add them into the list.
            log_data = {
                "id" : row_from_db["trips.id"],  #logs.__ because id overlaps with id in other tables
                "text" : row_from_db["text"],
                "user_id" : row_from_db['user_id'],
                "created_at" : row_from_db["trips.created_at"],
                "updated_at" : row_from_db["trips.updated_at"]
                
            }
            user.trips.append( travelinfo.Travelinfo( log_data ) ) #call log class, then call Log constructor
        return user     #returns an object with a list of logs inside 


# REGISTRATION
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO user ( first_name , last_name  , email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s ,NOW() , NOW() );"
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result
    

#LOGIN
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        #result is a list of dictionaries

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0]) 

    @staticmethod
    def validate_user(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True # we assume this is true

        currentUser = User.get_by_email({'email':user['email']})
        if currentUser: #falsy/truthy -> get_by_email returns either empty tuple or a tuple if it already exists
            flash("User already exists")
            is_valid = False
        if len(user['fname']) < 2:
            flash("First name is required.")
            is_valid = False
        if len(user['lname']) < 2:
            flash("Last name is required.")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password should be a minimum of 8 characters.")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True # we assume this is true
        if len(user['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password is required.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []      # Create an empty list to append instances of users
        for user in results: # Iterate over the db results and create instances of users with cls.
            users.append( cls(user) )
        return users #returns list of class objects (list of dictionaries)
            

    @classmethod
    def get_one(cls, data):
        # data = {'id': id}
        query = "SELECT * FROM user WHERE id = %(id)s ;" #%(id)s is the key of the dictionary data and returns id
        results = connectToMySQL(cls.db).query_db(query, data) #query_db returns list of objects
        print ("here",results)
        return cls(results[0])   

    @classmethod
    def delete(cls, data ):     # class method to remove one user from the database
        query = "DELETE FROM user WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod     # class method to edit one user in the database
    def update(cls, data ):
        query = "UPDATE user SET first_name = %(fname)s , last_name = %(lname)s  , email = %(email)s , updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db( query, data )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"