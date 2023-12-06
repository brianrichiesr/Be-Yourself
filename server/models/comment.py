from config import (
    SerializerMixin, 
    metadata, 
    association_proxy, 
    validates,
    db)

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