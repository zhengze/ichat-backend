from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db


ROLE_USER = 0
ROLE_ADMIN = 1


class UserGroup(db.Model):
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    gname = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('own_groups', lazy='dynamic'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __repr__(self):
        return '<UserGroup %r>' % self.gname


class UserGroupMember(db.Model):
    __tablename__ = 'user_group_member'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    group = db.relationship(
        'UserGroup',
        backref=db.backref(
            'joined_groups',
            lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('members', lazy='dynamic'))
    isdelete = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __repr__(self):
        return '<UserGroupMember %r>' % self.id


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.Unicode(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
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


class Friend(db.Model):
    __tablename__ = "friend"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        backref=db.backref(
            'users',
            lazy='dynamic'),
        foreign_keys=[user_id])
    friend = db.relationship(
        'User',
        backref=db.backref(
            'friends',
            lazy='dynamic'),
        foreign_keys=[friend_id])
    isdelete = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __repr__(self):
        return '<Friend %r>' % (self.id)


class UserChatLog(db.Model):
    __tablename__ = "user_chat_log"

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship(
        'User',
        backref=db.backref(
            'fuserchatlog',
            lazy='dynamic'),
        foreign_keys=[from_user_id])
    to_user = db.relationship(
        'User',
        backref=db.backref(
            'tuserchatlog',
            lazy='dynamic'),
        foreign_keys=[to_user_id])
    message = db.Column(db.String(128))
    isread = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    __mapper_args__ = {
        'order_by': create_time.desc()
    }

    def __init__(self, from_user, to_user, message):
        self.from_user = from_user
        self.to_user = to_user
        self.message = message

    def __repr__(self):
        return '<UserChatLog %r>' % self.message


class UserGroupChatLog(db.Model):
    __tablename__ = "user_group_chat_log"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    group = db.relationship(
        'UserGroup', backref=db.backref(
            'chatlogs', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        backref=db.backref(
            'groupchatlog',
            lazy='dynamic'))
    message = db.Column(db.String(128))
    isread = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    __mapper_args__ = {
        'order_by': create_time.desc()
    }

    def __repr__(self):
        return '<UserGroupChatLog %r>' % self.message
