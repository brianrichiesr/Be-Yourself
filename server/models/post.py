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
    honoree_id = db.Column(db.Integer, nullable=False)

    # Relationships
    comments = db.relationship('Comment', back_populates='post', order_by="desc(Comment.created_at)", cascade='all, delete-orphan')
    comment_authors = association_proxy('comments', 'user')
    post_author = db.relationship('User', back_populates='posts_authored')

    # Serialization
    serialize_rules = ('-users.posts_commented_on', '-comments.post', '-comments.post_id', '-comments.user_id')

    # Add validations
    @validates('description')
    def validate_description(self, _, description):
        if not isinstance(description, str) :
            raise TypeError('Description must be a String')
        elif len(description) < 1:
            raise ValueError('Description must be at least one letter long')
        return description

    def __repr__(self):
        return f'<Post {self.id}, {self.description} />'