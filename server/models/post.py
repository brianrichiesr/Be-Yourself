from config import (
    SerializerMixin, 
    metadata, 
    association_proxy, 
    validates,
    db)

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