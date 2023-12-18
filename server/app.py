#!/usr/bin/env python3

# Standard library imports

# Remote library imports
import json
import sqlite3
from flask import request, make_response, jsonify
from flask_restful import Resource
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    current_user,
    get_jwt,
    # set_access_cookies,
    # set_refresh_cookies,
    # unset_access_cookies,
    # unset_refresh_cookies,
    )
from sqlalchemy import desc
import requests

# Local imports
from config import app, db, api

# Add your model imports
from models.user import User
from models.user import user_connections
from models.post import Post
from models.comment import Comment


# Views go here!

# Helper function to convert sql objects to dict
def convert_sql(sq_list):
    # Assign empty list to variable
    r_list = []
    # Iterate through argument passed
    for response in sq_list:
        # Create a dict and assign values to keys
        connect = {
            "id": response[0],
            "sender_id": response[1],
            "receiver_id": response[2],
            "status": response[3],
            "reason": response[4],    
        }
        # Append dict to previously created list
        r_list.append(connect)
    # Return list of dicts
    return r_list

def get_pending_sent(user):
    pending_sent = []
    for connect in list(user.pending_sent_connections):
        connect_obj = {
            "id": connect.id,
            "user_name": connect.user_name,

        }
        pending_sent.append(connect_obj)
    return pending_sent

def get_pending_received(user):
    pending_received = []
    for connect in list(user.pending_received_connections):
        connect_obj = {
            "id": connect.id,
            "user_name": connect.user_name,

        }
        pending_received.append(connect_obj)
    return pending_received

def get_accepted_sent(user):
    accepted_sent = []
    for connect in list(user.accepted_sent_connections):
        connect_obj = {
            "id": connect.id,
            "user_name": connect.user_name,

        }
        accepted_sent.append(connect_obj)
    return accepted_sent

def get_accepted_received(user):
    accepted_received = []
    for connect in list(user.accepted_received_connections):
        connect_obj = {
            "id": connect.id,
            "user_name": connect.user_name,

        }
        accepted_received.append(connect_obj)
    return accepted_received

# Function for to connect to '/' route
# @app.route('/')
# def index():
#     return '<h1>Be Yourself Server Side Route</h1>'

# Restful routes for 'User' model
class Users(Resource):

    def get(self):
        try:
            # Create empty list
            u_list = []
            # Query 'User' table and assign all users to variable
            users = User.query
            # Iterate through variable
            for user in users:
                # Convert each object in users to dict and do not return 'password'
                u_list.append(user.to_dict(rules=('-password',)))
            # Return response object and 200 status
            return make_response(u_list, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def post(self):
        try:
            # Convert data from request body to json object
            data = json.loads(request.data)
            # Query 'User' table for user by the unique email passed
            user = User.query.filter_by(email=data["email"]).first()
            # If there is a user in table with that email
            if user:
                # Return response object and 400 status
                return make_response(
                    {
                        "errors": "Invalid Credentials"
                    }, 403
                )
            # Create a new user with 'data' without 'password'
            new_user = User(
                user_name = data["user_name"],
                email = data["email"]
            )
            # Assign 'password' from 'data' to newly created user to utilize encryption capability of 'User'
            new_user.password = data["password"]
            # Add new user to session and commit new user to db table
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=new_user.id)
            response = {"user": new_user.to_dict(rules=('-password',))}
            response['access_token'] = access_token
            # return make_response(response, 200)
            # Return response object without 'password' and 201 status
            return make_response(response, 201)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
# Add GET and POST functionality to '/users' route
api.add_resource(Users, '/api/v1/users')

class UserByID(Resource):

    def get(self, id):
        try:
            # Query 'User' table for user with 'id' passed
            user = db.session.get(User, id)
            # If a user exists, return user in dict without 'password'
            if user:
                # Use many-to-many relationships to grab connections info
                pending_sent = get_pending_sent(user)
                pending_received = get_pending_received(user)
                accepted_sent = get_accepted_sent(user)
                accepted_received = get_accepted_received(user)
                # Convert 'user' to dict and add connections info
                user = user.to_dict(rules=('-password',))
                user["pending_sent"] = pending_sent
                user["pending_received"] = pending_received
                user["accepted_sent"] = accepted_sent
                user["accepted_received"] = accepted_received
                return make_response(user, 200)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "User Not Found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def patch(self, id):

        try:
            # Query 'User' table for user with 'id' passed
            user = db.session.get(User, id)
            # If user exists
            if user:
                # Convert data from request body to json object
                data = json.loads(request.data)
                # Iterate through 'data'
                for attr in data:
                    # If the attribute is not 'id'
                    if attr != "id":
                        # Set the value of the attribute to the value of corresponding key in 'data'
                        if attr == 'admin' or data[attr]:
                            setattr(user, attr, data[attr])
                # Add new user to session and commit new user to db table
                db.session.add(user)
                db.session.commit()
                access_token = create_access_token(identity=user.id)
                response = {"user": user.to_dict(rules=('-password',))}
                response['access_token'] = access_token
                # Return response object without 'password' and 200 status
                return make_response(response, 200)
            else:
                # Else return error in response object and 404 status
                return make_response(
                    {"errors": "User not found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def delete(self,id):

        try:
            # Query 'User' table for user with 'id' passed
            user = db.session.get(User, id)
            # If user exists
            if user:
                # Create a connection to the 'user_connections' table
                connection = sqlite3.connect("instance/app.db")
                cursor = connection.cursor()
                # Delete any row where the sender or receiver of a request to connect as 'id' that matches id passed
                cursor.execute(
                    '''DELETE FROM user_connections WHERE sender_id = (?)''',
                (id,))
                cursor.execute(
                    '''DELETE FROM user_connections WHERE receiver_id = (?)''',
                (id,))
                # Commit changes and close connection
                connection.commit()
                connection.close()
                posts = Post.query.filter_by(honoree_id=id).all()
                for post in posts:
                    db.session.delete(post)
                # Then delete user and commit changes
                db.session.delete(user)
                db.session.commit()
                # Return empty response object and 204 status
                return make_response({}, 204)
            else:
                # Else return error in response object and 404 status
                return make_response(
                    {"errors": "User not found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
# Add GET, PATCH and DELETE functionality to '/users/<int:id>' route
api.add_resource(UserByID, '/api/v1/users/<int:id>')

# Restful routes for 'Post' model
class Posts(Resource):
    @jwt_required()
    def get(self):
        try:
            # current_user = get_jwt_identity()
            # print(f"Current - {current_user}")
            # Create empty list
            p_list = []
            # Query 'Post' table and assign all posts to variable
            posts = Post.query.order_by(desc("id"))
            # Iterate through variable
            for post in posts:
                # Convert each object in posts to dict
                honoree = db.session.get(User, post.honoree_id)
                post_to_be_displayed = post.to_dict(rules=('-user_id',))
                post_to_be_displayed["honoree"] = honoree.to_dict()
                p_list.append(post_to_be_displayed)
                # p_list.append(post.to_dict(rules=('-user_id',)))
            # Return response object and 200 status
            return make_response(p_list, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def post(self):
        try:
            # Convert data from request body to json object
            data = json.loads(request.data)
            # Create a new post with 'data' 
            honoree_id = data["honoree_id"]
            honoree = db.session.get(User, honoree_id)
            if honoree:
                new_post = Post(
                    description = data["description"],
                    image = data["image"],
                    user_id = data["user_id"],
                    honoree_id = honoree_id
                )
                # Add new post to session and commit new user to db table
                db.session.add(new_post)
                db.session.commit()
                # Return response object and 201 status
                return make_response(new_post.to_dict(), 201)
            else:
                return make_response(
                    {"errors": "Honoree Not Found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )

# Add GET and POST functionality to '/posts route
api.add_resource(Posts, '/api/v1/posts')

class PostByID(Resource):

    def get(self, id):
        try:
            # Query 'Post' table for post with 'id' passed
            post = db.session.get(Post, id)
            # If a post exists, return user in dict
            if post:
                honoree = db.session.get(User, post.honoree_id)
                post_to_be_displayed = post.to_dict()
                post_to_be_displayed["honoree"] = honoree.to_dict()
                return make_response(post_to_be_displayed, 200)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "Post Not Found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def patch(self, id):

        try:
             # Query 'Post' table for post with 'id' passed
            post = db.session.get(Post, id)
            # If post exists
            if post:
                # Convert data from request body to json object
                data = json.loads(request.data)
                # Iterate through 'data'
                for attr in data:
                    # If the attribute is not 'id'
                    if attr != "id":
                        # Set the value of the attribute to the value of corresponding key in 'data'
                        setattr(post, attr, data[attr])
                # Add new user to session and commit new user to db table
                db.session.add(post)
                db.session.commit()
                # Return response object without 'password' and 200 status
                return make_response(post.to_dict(), 200)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "Post not found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def delete(self,id):

        try:
            # Query 'Post' table for user with 'id' passed
            post = db.session.get(Post, id)
            # If post exists
            if post:
                # Delete post and commit changes
                db.session.delete(post)
                db.session.commit()
                # Return empty response object and 204 status
                return make_response({}, 204)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "Post not found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )

# Add GET, PATCH and DELETE functionality to '/posts/<int:id>' route        
api.add_resource(PostByID, '/api/v1/posts/<int:id>')


# Restful routes for 'Post' model
class Comments(Resource):

    def get(self):
        try:
            # Create empty list
            c_list = []
            # Query 'Comment' table and assign all comments to variable
            comments = Comment.query
            # Iterate through variable
            for comment in comments:
                # Convert each object in comments to dict
                c_list.append(comment.to_dict())
            # Return response object and 200 status
            return make_response(c_list, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def post(self):
        try:
            # Convert data from request body to json object
            data = json.loads(request.data)
            # Check to see if the post the comment is to be connected to exists, if not return error in response object and 404 status
            post = db.session.get('Post', data['post_id'])
            if not post:
                return make_response(
                    {"errors": "Post not found"}, 404
                )
            # Check to see if the user the comment is to be connected to exists, if not return error in response object and 404 status
            user = db.session.get('User', data['user_id'])
            if not user:
                return make_response(
                    {"errors": "User not found"}, 404
                )
            # Create a new post with 'data'
            new_comment = Comment(
                comment = data["comment"],
                created_at = datetime.now(),
                user_id = data["user_id"],
                post_id = data["post_id"]
            )
            # Add new comment to session and commit new user to db table
            db.session.add(new_comment)
            db.session.commit()
            # Return response object and 201 status
            return make_response(new_comment.to_dict(), 201)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )

# Add GET and POST functionality to '/comments route
api.add_resource(Comments, '/api/v1/comments')

class CommentByID(Resource):

    def get(self, id):
        try:
            # Query 'Post' table for user with 'id' passed
            comment = db.session.get(Comment, id)
            # If a comment exists, return user in dict
            if comment:
                return make_response(comment.to_dict(), 200)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "Comment Not Found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def patch(self, id):

        try:
            # Query 'Comment' table for comment with 'id' passed
            comment = db.session.get(Comment, id)
            # If comment exists
            if comment:
                # Convert data from request body to json object
                data = json.loads(request.data)
                # Check to see if the post the comment is to be connected to exists, if not return error in response object and 404 status
                post = db.session.get(Post, data['post_id'])
                if not post:
                    return make_response(
                        {"errors": "Post not found"}
                    )
                # Check to see if the user the comment is to be connected to exists, if not return error in response object and 404 status
                user = db.session.get(User, data['user_id'])
                if not user:
                    return make_response(
                        {"errors": "User not found"}
                    )
                # Iterate through 'data'
                for attr in data:
                    # If the attribute is not 'id'
                    if attr != "id":
                        # Set the value of the attribute to the value of corresponding key in 'data'
                        setattr(comment, attr, data[attr])
                # Add new user to session and commit new user to db table
                db.session.add(comment)
                db.session.commit()
                # Return response object without 'password' and 200 status
                return make_response(comment.to_dict(), 200)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "Comment not found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def delete(self,id):

        try:
            # Query 'Comment' table for user with 'id' passed
            comment = db.session.get(Comment, id)
            # Delete post and commit changes
            if comment:
                db.session.delete(comment)
                db.session.commit()
                # Return empty response object and 204 status
                return make_response({}, 204)
            # Else return error in response object and 404 status
            else:
                return make_response(
                    {"errors": "Comment not found"}, 404
                )
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )

# Add GET, PATCH and DELETE functionality to '/comments/<int:id>' route        
api.add_resource(CommentByID, '/api/v1/comments/<int:id>')

# App routes for 'user_connections' table
@app.route('/api/v1/user_connections', methods=['GET', 'POST'])
def u_connections():
    # Create a connection to the 'user_connections' table
    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    # If request calls for a 'GET' method
    if request.method == 'GET':

        try:
            # Grab all the rows from 'user_connections' table and assign them to variable
            results = cursor.execute(
                '''SELECT * FROM user_connections'''
            )
            # Pass 'results' to helper function and return list of dicts converted from sql objects
            response = convert_sql(results)
            # Return response object and 200 status
            return make_response(response, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    # If request calls for a 'POST' method
    elif request.method == 'POST':

        try:
            # Convert data from request body to json object
            data = json.loads(request.data)
            # Assign 'data' to variables
            sender_id = data["sender_id"]
            receiver_id = data["receiver_id"]
            reason = data["reason"]
            # Create new row in 'user_connections' with values from 'data' and assign connection to table in variable
            result = cursor.execute(
                '''INSERT INTO user_connections (sender_id, receiver_id, reason) VALUES (?, ?, ?)''',
                (sender_id, receiver_id, reason))
            # Commit the new row to table
            connection.commit()
            # Select newly created row by id using .lastrowid method of 'result' (Research better way to return the newly created row with its id)
            new_posts = cursor.execute(
                '''SELECT * FROM user_connections WHERE id = (?)''',
            (result.lastrowid,))
            # Pass new row to helper function
            response = convert_sql(new_posts)
            # Close connection
            connection.close()
            # Return response object and 200 status
            return make_response(response, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Close connection
            connection.close()
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/api/v1/user_connections/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def u_connection_by_id(id):
    # Create a connection to the 'user_connections' table
    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    # If request calls for a 'GET' method
    if request.method == 'GET':

        try:
            # Grab rows from 'user_connections' table by 'id' passed and assign it to variable
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE id = (?)''',
                (id,))
            # Pass sql object to helper function assign first result to variable
            response = convert_sql(results)
            # Close connection
            connection.close()
            # If row does not exist, return error and 404 status
            if not len(response):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            # Return response object and 200 status
            return make_response(response[0], 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Close connection
            connection.close()
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    # If request calls for a 'PATCH' method
    elif request.method == 'PATCH':

        try:
            # Grab rows from 'user_connections' table by 'id' passed and assign it to variable
            u_comms = cursor.execute(
                '''SELECT * FROM user_connections WHERE id = (?)''',
                (id,))
            # Pass sql object to helper function assign first result to variable
            result = convert_sql(u_comms)
            # If row does not exist, return error and 404 status
            if not len(result):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            response = result[0]
            # Convert data from request body to json object
            data = json.loads(request.data)
            # Iterate through 'data'
            for attr in data:
                # If key not 'id'
                if attr != "id":
                    # Set the value of the key to the value of corresponding key in 'data'
                    response[attr] = data[attr]
            # Update row with data from 'response'
            cursor.execute(
                '''UPDATE user_connections SET sender_id = (?), receiver_id = (?), status = (?), reason = (?) WHERE id = (?)''',
                (response["sender_id"], response["receiver_id"], response["status"], response["reason"], id))
            # Commit changes and close connection
            connection.commit()
            connection.close()
            # Return response object and 200 status
            return make_response(response, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Close connection
            connection.close()
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    # If request calls for a 'PATCH' method
    elif request.method == 'DELETE':

        try:
            # Delete row where id matches 'id' passed
            cursor.execute(
                '''DELETE FROM user_connections WHERE id = (?)''',
            (id,))
            # Commit changes and close connection
            connection.commit()
            connection.close()
            # Return response object and 200 status
            return make_response({}, 204)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/api/v1/user_connections_sender/<int:id>', methods=['GET'])
def u_connection_by_sender_id(id):
    # Create a connection to the 'user_connections' table
    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    # If request calls for a 'GET' method
    if request.method == 'GET':

        try:
            # Grab rows from 'user_connections' table where 'id' passed matches the row's 'sender_id' and assign it to variable
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE sender_id = (?)''',
                (id,))
            # Pass 'results' to helper function and assign to variable
            response = convert_sql(results)
            # Close connection
            connection.close()
            # If there is not at least one row is list
            if not len(response):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            # Return response object and 200 status
            return make_response(response, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Close connection
            connection.close()
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/api/v1/user_connections_receiver/<int:id>', methods=['GET'])
def u_connection_by_receiver_id(id):
     # Create a connection to the 'user_connections' table
    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    # If request calls for a 'GET' method
    if request.method == 'GET':

        try:
            # Grab rows from 'user_connections' table where 'id' passed matches the row's 'sender_id' and assign it to variable
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE receiver_id = (?)''',
                (id,))
            # Pass 'results' to helper function and assign to variable
            response = convert_sql(results)
            # Close connection
            connection.close()
            # If there is not at least one row is list
            if not len(response):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            # Return response object and 200 status
            return make_response(response, 200)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Close connection
            connection.close()
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/api/v1/user_login', methods=["POST"])
def login():
    try:
        data = json.loads(request.data)
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            data_pw = data["password"]
            access = user.verify(data_pw)
            if access:
                refresh_token = create_refresh_token(identity=user.id)
                access_token = create_access_token(identity=user.id)
                response = {"user": user.to_dict(rules=('-password',))}
                response['access_token'] = access_token
                response['refresh_token'] = refresh_token
                return make_response(response, 200)
        else:
            response = {
                "access_token": "",
                "message": "Invalid Credentials"
            }
            return make_response(response, 403)
        
    except (ValueError, AttributeError, TypeError) as e:
        return make_response(
            {"errors": [str(e)]}, 400
        )


@app.route('/api/v1/check_token')
@jwt_required()
def check_token():
    user = db.session.get(User, get_jwt_identity())
    if user:
        return make_response({"user": user.to_dict(rules=('-password',))}, 200)
    response = {
        "access_token": "",
        "msg": "Unauthorized Access"
    }
    return make_response(response, 403)

@app.route('/api/v1/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        id = get_jwt_identity()
        user = db.session.get(User, id)
        access_token = create_access_token(identity=id)
        response = {
            "user": user.to_dict(rules=('-password',)),
            "access_token": access_token
        }
        return make_response(response, 200)
    except Exception as e:
        return {"message": str(e)}, 400

@app.route('/api/v1/login_with_google', methods=["POST"])
def login_with_google():
    try:
        data = json.loads(request.data)
        req = requests.get(
            f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={data['access_token']}",
            headers={"Content-Type": "text"})
        res = req.json()
        verified_email = res['verified_email']
        if req.status_code == 200 and verified_email:
            email = res['email']
            print(f"Google - {email} - {verified_email} - {req.status_code}")
            user = User.query.filter_by(email=email).first()
            if user:      
                refresh_token = create_refresh_token(identity=user.id)
                access_token = create_access_token(identity=user.id)
                response = {"user": user.to_dict(rules=('-password',))}
                response['access_token'] = access_token
                response['refresh_token'] = refresh_token
                return make_response(response, 200)
            else:
                response = {
                    "access_token": "",
                    "message": "User not found"
                }
                return make_response(response, 401)
        else:
            response = {
                "access_token": "",
                "message": "Invalid Credentials"
            }
            return make_response(response, 403)
        
    except (ValueError, AttributeError, TypeError) as e:
        return make_response(
            {"errors": [str(e)]}, 400
        )


if __name__ == '__main__':
    app.run(port=5555, debug=True)

