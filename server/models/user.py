# Got assistance for User to User connection from code found in this repo:
# https://github.com/isaacwilhite/table-3-phase-4-project/blob/main/server/models.py
import re

from config import (
    SerializerMixin, 
    metadata, 
    association_proxy, 
    validates,
    db,
    flask_bcrypt)
from sqlalchemy.ext.hybrid import hybrid_property
from models.comment import Comment

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
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.String, nullable=False)

    # Relationships
    pending_sent_connections = db.relationship(
        'User', secondary = user_connections,
        primaryjoin=(id == user_connections.c.sender_id) & (user_connections.c.status == 'pending'),
        secondaryjoin=(id == user_connections.c.receiver_id) & (user_connections.c.status == 'pending'),
        backref = 'pending_received_connections'
    )

    accepted_sent_connections = db.relationship(
        'User', secondary = user_connections,
        primaryjoin=(id == user_connections.c.sender_id) & (user_connections.c.status == 'accepted'),
        secondaryjoin=(id == user_connections.c.receiver_id) & (user_connections.c.status == 'accepted'),
        backref = 'accepted_received_connections'
    )
    

    # Relationship mapping the user to related comments
    comments = db.relationship(
        'Comment', back_populates="user", cascade='all, delete-orphan')

    # Relationship mapping user to related posts
    post_comments = association_proxy('comments', 'post',
                              creator=lambda self: Comment(user_id=self.id))
    
    posts_authored = db.relationship('Post', back_populates='post_author', cascade='all, delete-orphan')

    # Serialization
    serialize_only = ('user_name', 'email', 'id')

    # Properties
    @hybrid_property
    def password(self):
        raise AttributeError("Passwords are private")
    
    @password.setter
    def password(self, new_password):
        pw_hash = flask_bcrypt.generate_password_hash(new_password).decode("utf-8")
        self._password = pw_hash
    
    def verify(self, password_to_be_checked):
        return flask_bcrypt.check_password_hash(self._password, password_to_be_checked)
    
    # Add validations
    @validates('user_name')
    def validate_user_name(self, _, user_name):
        if not isinstance(user_name, str) :
            raise TypeError('User Name must be a String')
        elif len(user_name) < 1:
            raise ValueError('User Name must be at least one letter long')
        return user_name
    
    @validates('email')
    def validate_email(self, _, email):
        if not isinstance(email, str) :
            raise TypeError('Email must be a String')
        elif len(email) < 1:
            raise ValueError('Email must be at least one letter long')
        elif not re.search(r'@', email):
            raise ValueError('Email must include "@" to be valid')
        return email
    

    def __repr__(self):
        return f'''<User Id: {self.id} Email: {self.email} User: {self.user_name}>'''