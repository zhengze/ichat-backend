from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .database import db


ROLE_USER = 0
ROLE_ADMIN = 1


class UserGroup(db.Model):
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __repr__(self):
        return '<UserGroup %r>' % self.group_name


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.Unicode(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    contact_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    user_group = db.relationship('UserGroup',
                                 backref=db.backref('users', lazy='dynamic'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(self, username, password):
        self.username = username
        self.password = self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        return generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class UserChatLog(db.Model):
    __tablename__ = "user_chat_log"

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship(
        'User',
        backref=db.backref(
            'fromchatlog',
            lazy='dynamic'),
        foreign_keys=[from_user_id])
    to_user = db.relationship(
        'User',
        backref=db.backref(
            'tochatlog',
            lazy='dynamic'),
        foreign_keys=[to_user_id])
    message = db.Column(db.String(128))
    isread = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(self, from_user, to_user, message):
        self.from_user = from_user
        self.to_user = to_user
        self.message = message

    def __repr__(self):
        return '<UserChatLog %r>' % self.message


class UserGroupChatLog(db.Model):
    __tablename__ = "user_group_chat_log"

    id = db.Column(db.Integer, primary_key=True)
    from_group = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(128))
    has_read = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __repr__(self):
        return '<UserGroupChatLog %r>' % self.message
