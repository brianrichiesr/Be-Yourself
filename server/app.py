#!/usr/bin/env python3

# Standard library imports

# Remote library imports
import json
import sqlite3
from flask import request, make_response, jsonify
from flask_restful import Resource
from datetime import datetime

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

# Function for to connect to '/' route
@app.route('/')
def index():
    return '<h1>Be Yourself Server</h1>'

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
                    }, 400
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
            # Return response object without 'password' and 201 status
            return make_response(new_user.to_dict(rules=("-password",)), 201)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
# Add GET and POST functionality to '/users' route
api.add_resource(Users, '/users')

class UserByID(Resource):

    def get(self, id):
        try:
            # Query 'User' table for user with 'id' passed
            user = db.session.get(User, id)
            # If a user exists, return user in dict without 'password'
            if user:
                return make_response(user.to_dict(rules=('-password',)), 200)
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
                        setattr(user, attr, data[attr])
                # Add new user to session and commit new user to db table
                db.session.add(user)
                db.session.commit()
                # Return response object without 'password' and 200 status
                return make_response(user.to_dict(rules=("-password",)), 200)
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
api.add_resource(UserByID, '/users/<int:id>')

# Restful routes for 'Post' model
class Posts(Resource):

    def get(self):
        try:
            # Create empty list
            p_list = []
            # Query 'Post' table and assign all posts to variable
            posts = Post.query
            # Iterate through variable
            for post in posts:
                # Convert each object in posts to dict
                p_list.append(post.to_dict())
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
            new_post = Post(
                description = data["description"],
                image = data["image"],
                user_id = data["user_id"]
            )
            # Add new post to session and commit new user to db table
            db.session.add(new_post)
            db.session.commit()
            # Return response object and 201 status
            return make_response(new_post.to_dict(), 201)
        # If functionality in try fails, raise error and 400 status
        except (ValueError, AttributeError, TypeError) as e:
            # Remove staged changes
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )

# Add GET and POST functionality to '/posts route
api.add_resource(Posts, '/posts')

class PostByID(Resource):

    def get(self, id):
        try:
            # Query 'Post' table for post with 'id' passed
            post = db.session.get(Post, id)
            # If a post exists, return user in dict
            if post:
                return make_response(post.to_dict(), 200)
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
api.add_resource(PostByID, '/posts/<int:id>')


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
api.add_resource(Comments, '/comments')

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
api.add_resource(CommentByID, '/comments/<int:id>')

# App routes for 'user_connections' table
@app.route('/user_connections', methods=['GET', 'POST'])
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


@app.route('/user_connections/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
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


@app.route('/user_connections_sender/<int:id>', methods=['GET'])
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


@app.route('/user_connections_receiver/<int:id>', methods=['GET'])
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


if __name__ == '__main__':
    app.run(port=5555, debug=True)

