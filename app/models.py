from app import db

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    email = db.Column(db.String(254), unique=True, index=True)
    phone_number = db.Column(db.String(15), unique=True, index=True)
    category = db.Column(db.Integer)
    can_contact = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return "<Lead {}>".format(self.email)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(300))
    slug = db.Column(db.String(100), unique=True, index=True)
    author_name = db.Column(db.String(70))
    author_handle = db.Column(db.String(70))
    title = db.Column(db.String(70))
    description = db.Column(db.String(155))
    category = db.Column(db.Integer)
    section = db.Column(db.String(50))
    tags = db.Column(db.String(100))
    image_url = db.Column(db.String(300))
    published_time = db.Column(db.DateTime)
    modified_time = db.Column(db.DateTime)
    views = db.relationship('Log', backref='content', lazy='select')

    def __repr__(self):
        return "<Content {}>".format(self.slug)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    cookie_uuid = db.Column(db.String(36))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return "<Log {}-{}>".format(self.content_id, self.timestamp)