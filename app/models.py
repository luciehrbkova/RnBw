from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    boards = db.relationship('Board', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}'.format(self.name)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Board {}'.format(self.title)