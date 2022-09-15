# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

from flask_app import app


from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)   

import re	# the regex module

class Travelinfo: # model the class after the user table from  database
    
    db='travel' #database (in mySQL workbench)

    def __init__( self , data ):
        self.id = data['id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']  # hidden input 



    @classmethod
    def save(cls, data ):
        query = "INSERT INTO travelinfo ( text , user_id, created_at , updated_at ) VALUES ( %(text)s , %(user_id)s , NOW() , NOW() );"
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result
    
    @classmethod     # class method to remove one travel log from the database
    def delete(cls, data ):
        query = "DELETE FROM travelinfo WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_all(cls):

        query = """
        SELECT * FROM post 
        LEFT JOIN user ON post.user_id = user.id
        ORDER BY post.created_at DESC;
        """

        results = connectToMySQL(cls.db).query_db(query)

        travellogs = []      # Create an empty list to append instances of travel logs
        
        for log in results: # Iterate over the db results and create instances of travel logs with cls.
            one_log = cls(log)


            user_data = {
                "id":log["user.id"], 
                "first_name":log["first_name"], 
                "last_name":log["last_name"],
                "email":log["email"],
                "password":log["password"],
                "created_at" :log['user.created_at'],
                "updated_at": log['user.updated_at']
            }

            one_log.user = user.User(user_data)
            travellogs.append(one_log)
        return travellogs #returns list of class objects (list of dictionaries)



    
    def validate_log(post):
        is_valid = True # we assume this is true
        if len(post['text']) < 1:
            flash("Text must not be blank.")
            is_valid = False
        return is_valid




    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM travelinfo WHERE id = %(id)s ;" #%(id)s is the key of the dictionary data and returns id
        results = connectToMySQL(cls.db).query_db(query, data) #query_db returns list of objects
        return cls(results[0])   


    @classmethod     # if logged in as user, can delete log
    def delete(cls, data ):
        query = "DELETE FROM travelinfo WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod     # class method to edit one log in the database
    def update(cls, data ):
        query = "UPDATE travelinfo SET text = %(text)s, created_at =NOW(), updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db( query, data )


