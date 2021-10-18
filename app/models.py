from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    email = db.Column(db.String(254), unique=True, index=True)
    category = db.Column(db.String(10))
    can_contact = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(300))
    slug = db.Column(db.String(100), unique=True)
    author_name = db.Column(db.String(70))
    author_handle = db.Column(db.String(70))
    title = db.Column(db.String(70))
    description = db.Column(db.String(155))
    category = db.Column(db.String(10))
    section = db.Column(db.String(50))
    tags = db.Column(db.String(100))
    views = db.Column(db.Integer)
    image_url = db.Column(db.String(300))
    published_time = db.Column(db.DateTime)
    modified_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Content {}>".format(self.slug)