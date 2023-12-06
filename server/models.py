# server/models.py
# https://github.com/isaacwilhite/table-3-phase-4-project/blob/main/server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, flask_bcrypt, metadata

user_connections = db.Table(
    'user_connections',
    db.Column('sender_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('receiver_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('status', db.String, default='pending'),
    db.Column('reason', db.String)
)


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.String, nullable=False)

    pending_sent_connections = db.relationship(
        'User', secondary = user_connections,
        primaryjoin=(id == user_connections.c.sender_id) & (user_connections.c.status == 'pending'),
        secondaryjoin=(id == user_connections.c.receiver_id) & (user_connections.c.status == 'pending'),
        back_populates = 'accepted_sent_connections'
    )

    accepted_sent_connections = db.relationship(
        'User', secondary = user_connections,
        primaryjoin=(id == user_connections.c.sender_id) & (user_connections.c.status == 'accepted'),
        secondaryjoin=(id == user_connections.c.receiver_id) & (user_connections.c.status == 'accepted'),
        back_populates = 'pending_sent_connections'
    )
    

    # Relationship mapping the user to related comments
    comments = db.relationship(
        'Comment', back_populates="user", cascade='all, delete-orphan')

    # Relationship mapping user to related posts
    posts = association_proxy('comments', 'post')

    
    serialize_rules = (
        '-accepted_sent_connections',
        '-pending_sent_connections',
        '-rejected_sent_connections',
        '-pending_received_connections',
        '-rejected_received_connections',
        '-accepted_received_connections',
        '-comments.user',
        '-posts.user'
    )

    @hybrid_property
    def password(self):
        raise AttributeError("Passwords are private")
    
    @password.setter
    def password(self, new_password):
        pw_hash = flask_bcrypt.generate_password_hash(new_password).decode("utf-8")
        self._password = pw_hash
    
    def verify(self, password_to_be_checked):
        return flask_bcrypt.check_password_hash(self._password, password_to_be_checked)


    def __repr__(self):
        return f'''<User {self.id},
            First: {self.first_name}
            Last: {self.last_name}
            Email: {self.email} />'''


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    image = db.Column(db.String)
    status = db.Column(db.String, default='pending')

    # Foreign key to store the user id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship mapping post to related user
    comments = db.relationship('Comment', back_populates='post')
    users = association_proxy('comments', 'user')

    serialize_rules = ('-user.posts', '-comments.post')

    def __repr__(self):
        return f'<Post {self.id}, {self.description} />'


class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Foreign key to store the user id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    # Relationship mapping the review to related user
    user = db.relationship('User', back_populates="comments")
    post = db.relationship('Post', back_populates="comments")

    serialize_rules = ('-user.comments', '-post.comments')

    def __repr__(self):
        return f'<Comment {self.id}, {self.comment} />'