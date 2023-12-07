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



fake = Faker()

def create_users():
    users = []
    for _ in range(10):

        c = User(
            user_name=fake.name(),
            email=fake.email(),
        )

        c.password = "password"

        users.append(c)

    return users



def create_posts(users):
    posts = []
    for _ in range(20):
        p = Post(
            user_id=rc([user.id for user in users]),
            description = fake.sentence(),
            image = fake.image_url(),
            # status = fake.sentence()
        )
        posts.append(p)

    return posts



def create_comments(users, posts):
    comments = []

    for _ in range(40):
        c = Comment(
            user_id=rc([user.id for user in users]),
            post_id=rc([post.id for post in posts]),
            comment = fake.sentence(),
            created_at = fake.date_time()
        )
        comments.append(c)

    return comments

def create_user_connections(users):


    #! Delete tables if they exist, recreate them for fresh data
    with connection:
        cursor.execute(f'''DROP TABLE IF EXISTS {user_connections}''')
        connection.commit()
                

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


    u_cs = []

    for _ in range(8):
        sender_id=rc([user.id for user in users])
        receiver_id=rc([user.id for user in users])
        reason = fake.sentence()
        print(f"")
        cursor.execute(
            '''INSERT INTO user_connections (sender_id, receiver_id, reason)VALUES (?, ?, ?);''',
            (sender_id, receiver_id, reason))
        connection.commit()

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