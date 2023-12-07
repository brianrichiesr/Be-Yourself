#!/usr/bin/env python3

# Standard library imports

# Remote library imports
import json
from flask import request, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models.user import User
from models.user import user_connections
from models.post import Post
from models.comment import Comment


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

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
            
            new_user = User(
                first_name = data["first_name"],
                last_name = data["last_name"],
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
    
    # def patch(self, id):
    #     try:
    #         user = db.session.get(User, id)
    #         if user:
    #             data = json.loads(request.data)
    #             for attr in data:
    #                 setattr(user, attr, data[attr])
    #             db.session.add(user)
    #             db.session.commit()
    #             r_list = []
    #             rentals = Rental.query.filter(Rental.user_id==user.id)
    #             for rental in rentals:
    #                 r_list.append(db.session.get(Movie, rental.movie_id).to_dict())
    #             user = user.to_dict(rules=("-password",))
    #             user["rentals"] = r_list
    #             return make_response(user, 200)
    #         else:
    #             return make_response(
    #                 {"errors": "Update unsuccessful"}, 400
    #             )
    #     except (ValueError, AttributeError, TypeError) as e:
    #         db.session.rollback()
    #         return make_response(
    #             {"errors": [str(e)]}, 400
    #         )
    
    def delete(self,id):
        try:
            user = db.session.get(User, id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return make_response({}, 204)
            else:
                return make_response(
                    {"errors": "Delete unsuccessful"}, 400
                )
        except (ValueError, AttributeError, TypeError) as e:
            db.session.rollback()
            return make_response(
                {"errors": [str(e)]}, 400
            )
        
api.add_resource(UserByID, '/users/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

