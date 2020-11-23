from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    boards = db.relationship('Board', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}'.format(self.name)
    #password hash set and check
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card', backref='motherboard', lazy='dynamic')
    def __repr__(self):
        return '<Board {}'.format(self.title)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(20))
    date = db.Column(db.Date, index=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))

    def __repr__(self):
        return '<Card {}'.format(self.id)