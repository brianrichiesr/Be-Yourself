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

    # Serialization
    serialize_rules = ('-user.comments', '-post.comments')

    # Add validations
    @validates('comment')
    def validate_comment(self, _, comment):
        if not isinstance(comment, str) :
            raise TypeError('Comment must be a String')
        elif len(comment) < 1:
            raise ValueError('Comment must be at least one letter long')
        return comment

    def __repr__(self):
        return f'<Comment {self.comment}, Id: {self.id}, Post Id: {self.post_id} />'