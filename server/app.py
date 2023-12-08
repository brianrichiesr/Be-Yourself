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

def convert_sql(sq_list):
    r_list = []
    for response in sq_list:
        connect = {
            "id": response[0],
            "sender_id": response[1],
            "receiver_id": response[2],
            "status": response[3],
            "reason": response[4],    
        }
        r_list.append(connect)
    return r_list

@app.route('/')
def index():
    return '<h1>Be Yourself Server</h1>'

class Users(Resource):
    def get(self):
        try:
            u_list = []
            users = User.query
            for user in users:
                u_list.append(user.to_dict(rules=('-password',)))
            return make_response(u_list, 200)
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def post(self):
        try:
            data = json.loads(request.data)
            user = User.query.filter_by(email=data["email"]).first()
            if user:
                db.session.rollback()
                return make_response(
                    {
                        "errors": "Invalid Credentials"
                    }
                )
            
            new_user = User(
                user_name = data["user_name"],
                email = data["email"]
            )

            new_user.password = data["password"]

            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(rules=("-password",)), 201)
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
api.add_resource(Users, '/users')

class UserByID(Resource):
    def get(self, id):
        try:
            user = db.session.get(User, id)
            if user:
                return make_response(user.to_dict(rules=('-password',)), 200)
            else:
                return make_response(
                    {"errors": "User Not Found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def patch(self, id):
        try:
            user = db.session.get(User, id)
            if user:
                data = json.loads(request.data)
                for attr in data:
                    if attr != "id":
                        setattr(user, attr, data[attr])
                db.session.add(user)
                db.session.commit()
                return make_response(user.to_dict(rules=("-password",)), 200)
            else:
                db.session.rollback()
                return make_response(
                    {"errors": "User not found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def delete(self,id):
        try:
            user = db.session.get(User, id)
            if user:
                connection = sqlite3.connect("instance/app.db")
                cursor = connection.cursor()
                cursor.execute(
                    '''DELETE FROM user_connections WHERE sender_id = (?)''',
                (id,))
                cursor.execute(
                    '''DELETE FROM user_connections WHERE receiver_id = (?)''',
                (id,))
                connection.commit()
                connection.close()
                db.session.delete(user)
                db.session.commit()
                return make_response({}, 204)
            else:
                db.session.rollback()
                return make_response(
                    {"errors": "User not found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
        
api.add_resource(UserByID, '/users/<int:id>')



class Posts(Resource):
    def get(self):
        try:
            p_list = []
            posts = Post.query
            for post in posts:
                p_list.append(post.to_dict())
            return make_response(p_list, 200)
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def post(self):
        try:
            data = json.loads(request.data)
            
            new_post = Post(
                description = data["description"],
                image = data["image"],
                user_id = data["user_id"]
            )

            db.session.add(new_post)
            db.session.commit()
            return make_response(new_post.to_dict(), 201)
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
api.add_resource(Posts, '/posts')

class PostByID(Resource):
    def get(self, id):
        try:
            post = db.session.get(Post, id)
            if post:
                return make_response(post.to_dict(), 200)
            else:
                return make_response(
                    {"errors": "Post Not Found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def patch(self, id):
        try:
            post = db.session.get(Post, id)
            if post:
                data = json.loads(request.data)
                for attr in data:
                    if attr != "id":
                        setattr(post, attr, data[attr])
                db.session.add(post)
                db.session.commit()
                return make_response(post.to_dict(), 200)
            else:
                return make_response(
                    {"errors": "Post not found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def delete(self,id):
        try:
            post = db.session.get(Post, id)
            if post:
                db.session.delete(post)
                db.session.commit()
                return make_response({}, 204)
            else:
                return make_response(
                    {"errors": "Post not found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
        
api.add_resource(PostByID, '/posts/<int:id>')



class Comments(Resource):
    def get(self):
        try:
            c_list = []
            comments = Comment.query
            for comment in comments:
                c_list.append(comment.to_dict())
            return make_response(c_list, 200)
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def post(self):
        try:
            data = json.loads(request.data)
            post = db.session.get('Post', data['post_id'])
            if not post:
                return make_response(
                    {"errors": "Post not found"}
                )
            user = db.session.get('User', data['user_id'])
            if not user:
                return make_response(
                    {"errors": "User not found"}
                )
            new_comment = Comment(
                comment = data["comment"],
                created_at = datetime.now(),
                user_id = data["user_id"],
                post_id = data["post_id"]
            )

            db.session.add(new_comment)
            db.session.commit()
            return make_response(new_comment.to_dict(), 201)
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
api.add_resource(Comments, '/comments')

class CommentByID(Resource):
    def get(self, id):
        try:
            comment = db.session.get(Comment, id)
            if comment:
                return make_response(comment.to_dict(), 200)
            else:
                return make_response(
                    {"errors": "Comment Not Found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def patch(self, id):
        try:
            comment = db.session.get(Comment, id)
            if comment:
                data = json.loads(request.data)
                post = db.session.get(Post, data['post_id'])
                if not post:
                    return make_response(
                        {"errors": "Post not found"}
                    )
                user = db.session.get(User, data['user_id'])
                if not user:
                    return make_response(
                        {"errors": "User not found"}
                    )
                for attr in data:
                    if attr != "id":
                        setattr(comment, attr, data[attr])
                db.session.add(comment)
                db.session.commit()
                return make_response(comment.to_dict(), 200)
            else:
                return make_response(
                    {"errors": "Comment not found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    
    def delete(self,id):
        try:
            comment = db.session.get(Comment, id)
            if comment:
                db.session.delete(comment)
                db.session.commit()
                return make_response({}, 204)
            else:
                return make_response(
                    {"errors": "Comment not found"}, 404
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
        
api.add_resource(CommentByID, '/comments/<int:id>')


@app.route('/user_connections', methods=['GET', 'POST'])
def u_connections():
    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    if request.method == 'GET':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections'''
            )
            response = convert_sql(results)
            return make_response(response, 200)
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'POST':
        try:
            data = json.loads(request.data)
            sender_id = data["sender_id"]
            receiver_id = data["receiver_id"]
            reason = data["reason"]
            result = cursor.execute(
                '''INSERT INTO user_connections (sender_id, receiver_id, reason) VALUES (?, ?, ?)''',
                (sender_id, receiver_id, reason))
            connection.commit()
            new_posts = cursor.execute(
                '''SELECT * FROM user_connections WHERE id = (?)''',
            (result.lastrowid,))
            response = convert_sql(new_posts)
            connection.close()
            return make_response(response, 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/user_connections/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def u_connection_by_id(id):

    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    if request.method == 'GET':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE id = (?)''',
                (id,))
            response = convert_sql(results)
            connection.close()
            if not len(response):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            return make_response(response, 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'PATCH':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE id = (?)''',
                (id,))
            response = convert_sql(results)[0]
            if not len(response):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            data = json.loads(request.data)
            for attr in data:
                if attr != "id":
                    response[attr] = data[attr]
            cursor.execute(
                '''UPDATE user_connections SET sender_id = (?), receiver_id = (?), status = (?), reason = (?) WHERE id = (?)''',
                (response["sender_id"], response["receiver_id"], response["status"], response["reason"], id))
            connection.commit()
            connection.close()
            return make_response(response, 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'DELETE':
        try:
            cursor.execute(
                '''DELETE FROM user_connections WHERE id = (?)''',
            (id,))
            connection.commit()
            connection.close()
            return make_response({}, 204)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/user_connections_sender/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def u_connection_by_sender_id(id):

    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    if request.method == 'GET':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE sender_id = (?)''',
                (id,))
            r_list = []
            for result in results:
                connect = {
                    "id": result[0],
                    "sender_id": result[1],
                    "receiver_id": result[2],
                    "status": result[3],
                    "reason": result[4],    
                }
                r_list.append(connect)
            connection.close()
            if not len(r_list):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            return make_response(r_list, 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'PATCH':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE sender_id = (?)''',
                (id,))
            r_list = []
            for result in results:
                connect = {
                    "id": result[0],
                    "sender_id": result[1],
                    "receiver_id": result[2],
                    "status": result[3],
                    "reason": result[4],    
                }
                r_list.append(connect)
            if not len(r_list):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            data = request.data
            for attr in data:
                setattr(r_list[0], attr, data)
            cursor.execute(
                '''UPDATE user_connections SET (sender_id, receiver_id, status, reason) VALUES (?, ?, ?, ?) WHERE sender_id = (?)''',
                (r_list[0].sender_id, r_list[0].receiver_id, r_list[0].status, r_list[0].reason, id))
            connection.commit()
            connection.close()
            return make_response(r_list[0].to_dict(), 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'DELETE':
        try:
            cursor.execute(
                '''DELETE FROM user_connections WHERE sender_id = (?)''',
            (id,))
            connection.commit()
            connection.close()
            return make_response({{}, 204})
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


@app.route('/user_connections_receiver/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def u_connection_by_receiver_id(id):

    connection = sqlite3.connect("instance/app.db")
    cursor = connection.cursor()
    if request.method == 'GET':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE receiver_id = (?)''',
                (id,))
            r_list = []
            for result in results:
                connect = {
                    "id": result[0],
                    "sender_id": result[1],
                    "receiver_id": result[2],
                    "status": result[3],
                    "reason": result[4],    
                }
                r_list.append(connect)
            connection.close()
            if not len(r_list):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            return make_response(r_list.to_dict(), 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'PATCH':
        try:
            results = cursor.execute(
                '''SELECT * FROM user_connections WHERE receiver_id = (?)''',
                (id,))
            r_list = []
            for result in results:
                connect = {
                    "id": result[0],
                    "sender_id": result[1],
                    "receiver_id": result[2],
                    "status": result[3],
                    "reason": result[4],    
                }
                r_list.append(connect)
            if not len(r_list):
                return make_response(
                    {"error": "User Connection not found"}, 404
                )
            data = request.data
            for attr in data:
                setattr(r_list[0], attr, data)
            cursor.execute(
                '''UPDATE user_connections SET (sender_id, receiver_id, status, reason) VALUES (?, ?, ?, ?) WHERE receiver_id = (?)''',
                (r_list[0].sender_id, r_list[0].receiver_id, r_list[0].status, r_list[0].reason, id))
            connection.commit()
            connection.close()
            return make_response(r_list[0].to_dict(), 200)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
    elif request.method == 'DELETE':
        try:
            cursor.execute(
                '''DELETE FROM user_connections WHERE receiver_id = (?)''',
            (id,))
            connection.commit()
            connection.close()
            return make_response({}, 204)
        except (ValueError, AttributeError, TypeError) as e:
            connection.close()
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )


if __name__ == '__main__':
    app.run(port=5555, debug=True)

