#!/usr/bin/env python
import sqlite3
import sys
sys.path.append('.')
connection = sqlite3.connect("instance/app.db")
cursor = connection.cursor()

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker
from sqlalchemy import insert

# Local imports
from config import app, db
# from app_setup import db
from models.user import User
from models.user import user_connections
from models.post import Post
from models.comment import Comment

# Assign 'Faker' module functionality to variable
fake = Faker()

# Function to create fake users
def create_users():
    # Empty list
    users = []
    # Iterate 10 times
    for _ in range(10):
        # Create a new user with fake data and assign to variable
        c = User(
            user_name=fake.name(),
            email=fake.email(),
        )
        # Assign password after user is instantiated to make use of encryption attribute
        c.password = "password"
        # Append new user to list
        users.append(c)
    # Return list
    return users


# Function to create fake posts
def create_posts(users):
    # Empty list
    posts = []
    # Iterate 20 times
    for _ in range(20):
        # Create a new post with fake data and assign to variable
        p = Post(
            user_id=rc([user.id for user in users]),
            description = fake.paragraph(),
            image = fake.image_url()
        )
        # Append new post to list
        posts.append(p)
    # Return list
    return posts


# Function to create fake comments
def create_comments(users, posts):
    # Empty list
    comments = []
    # Iterate 40 times
    for _ in range(40):
        # Create a new comment with fake data and assign to variable
        c = Comment(
            user_id=rc([user.id for user in users]),
            post_id=rc([post.id for post in posts]),
            comment = fake.sentence(),
            created_at = fake.date_time()
        )
        # Append new comment to list
        comments.append(c)
    # Return list
    return comments

# Function to create fake user connections
def create_user_connections(users):

    # Delete 'user_connections' if it exists
    with connection:
        cursor.execute(f'''DROP TABLE IF EXISTS {user_connections}''')
        connection.commit()
                
        # Recreate 'user_connections' table with schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_connections (
            id INTEGER PRIMARY KEY,
            sender_id int,
            receiver_id int,
            status varchar(255) DEFAULT 'pending',
            reason mediumtext,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
            );
        ''')

    # Empty list
    u_cs = []
    # Iterate 8 times
    for _ in range(8):
        # Assign fake data to variables
        sender_id=rc([user.id for user in users])
        receiver_id=rc([user.id for user in users])
        reason = fake.sentence()
        # Create a new user connection with fake data
        cursor.execute(
            '''INSERT INTO user_connections (sender_id, receiver_id, reason)VALUES (?, ?, ?);''',
            (sender_id, receiver_id, reason))
        # Commit new user connection
        connection.commit()
    # Close connection
    connection.close()
    # Return list
    return u_cs



if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        Post.query.delete()
        Comment.query.delete()
        
        print("Creating tables...")
        db.create_all()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding posts...")
        posts = create_posts(users)
        db.session.add_all(posts)
        db.session.commit()

        print("Seeding comments...")
        comments = create_comments(users, posts)
        db.session.add_all(comments)
        db.session.commit()

        print("Seeding user_connections...")
        user_connections = create_user_connections(users)
        db.session.add_all(user_connections)
        db.session.commit()

        print("Seeding complete!!!")
        
print("Flask app and SQLAlchemy imported in seed.py.")