from datetime import datetime

from .core import db
from .passwords import hash_password, verify_password


class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String)

    def __repr__(self):
        return '<User %r>' % self.id






def add_user(username, password):
    if not 6 <= len(username) <= 100:
        raise ValueError("To incorrect username length")

    if not 6 <= len(password) <= 72:
        raise ValueError("To incorrect password length")

    password_hash = hash_password(password)
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def user_login(username, password):
    if not 6 <= len(username) <= 100:
        raise ValueError("To incorrect username length")

    if not 6 <= len(password) <= 72:
        raise ValueError("To incorrect password length")

    user = User.query.where(User.username == username).one()

    if not verify_password(password, user.password_hash):
        raise IndentationError("Password is incorrect")

    return user