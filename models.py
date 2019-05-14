from app import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin
import re


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str(s))


post_tags = db.Table('post_tags', db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


#Post table
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(148))
    slug = db.Column(db.String(148), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title {},'.format(self.id, self.title)


#Tags table
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    post_id = db.Column(db.ForeignKey('posts.id'))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


#users manager
roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('users.id')), db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    social_id = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64))
    # role_ids = db.Column(db.ForeignKey('roles.id'))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    discription = db.Column(db.String(255))

    def __repr__(self):
        return '{}'.format(self.name)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text, nullable=False)
    # role_for_comment = db.Column(db.String(64))
    post_id = db.Column(db.ForeignKey('posts.id'))
    user_id = db.Column(db.ForeignKey('users.id'))
    # role_id = db.Column(db.ForeignKey('roles.id'))


    # def __init__(self, *args, **kwargs):
    #     super(Comment, self).__init__(*args, **kwargs)
    #
    # def __repr__(self):
    #     return '<Comment body: {}>'.format(self.body, self.post_id, self.user_id, self.role_for_comment)
    #
    #













