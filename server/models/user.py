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
    posts = association_proxy('comments', 'post')

    # Serialization
    serialize_only = ('email', 'first_name', 'last_name')

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
    @validates('first_name')
    def validate_first_name(self, _, first_name):
        if not isinstance(first_name, str) :
            raise TypeError('First Name must be a String')
        elif len(first_name) < 1:
            raise ValueError('First Name must be at least one letter long')
        return first_name
    
    @validates('last_name')
    def last_name(self, _, last_name):
        if not isinstance(last_name, str) :
            raise TypeError('Last Name must be a String')
        elif len(last_name) < 1:
            raise ValueError('Last Name must be at least one letter long')
        return last_name
    
    @validates('email')
    def validate_email(self, _, email):
        if not isinstance(email, str) :
            raise TypeError('Email must be a String')
        elif len(email) < 1:
            raise ValueError('Last Name must be at least one letter long')
        elif not re.search(r'@', email):
            raise ValueError('Email must include "@" to be valid')
        return email
    

    def __repr__(self):
        return (f'''<User Id: {self.id} Email: {self.email}>''')