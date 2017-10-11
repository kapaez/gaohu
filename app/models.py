# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request

import hashlib
import bleach
import time
from random import randint
from markdown import markdown
import json
from . import login_manager
from . import db
import random
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    @staticmethod
    def fake_fans(num):
        for i in range(num):
                follow = Follow(followed = User.query.filter_by(id=randint(1,63)).first(),
                                follower = User.query.filter_by(id=randint(1,63)).first())
                db.session.add(follow)
                db.session.commit()
                time.sleep(1)
                print 'ok'

    @staticmethod
    def follow_self():
        for i in User.query.all():
            if not i.is_following(i):
                i.follow(i)
                db.session.add(i)
                db.session.commit()


class Answer(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    Question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code','br'
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
db.event.listen(Answer.body, 'set', Answer.on_changed_body)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    answer = db.relationship('Answer',
                            foreign_keys=[Answer.Question_id],
                            backref=db.backref('question', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #用户个人信息相关列
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(64))
    avatar = db.Column(db.String(128))
    questions = db.relationship('Question',
                               foreign_keys=[Question.author_id],
                               backref=db.backref('author', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    answer = db.relationship('Answer',
                             foreign_keys=[Answer.author_id],
                             backref=db.backref('author', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    @property
    def followed_Answer(self):
            return Answer.query.join(Follow,Follow.followed_id == Answer.author_id).\
                    filter(Follow.follower_id == self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #生成确认token
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    #生成重设密码token
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    #对token进行检查，并修改confirm状态
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    #重设密码
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    #修改邮箱发送的token
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    #修改邮箱
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        #self.avatar_hash = hashlib.md5(
        #   self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    #权限检查，用户权限和需求权限相同，返回为真
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    #管理员权限检查，如果是管理员，则返回True
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @staticmethod
    def create_user():
        count = 0
        datas = json.load(open('G:/virtualenv/gaohu/gaohu/app/followers.json'))
        for data in datas:
            count += 1
            print count
            if datas[data]['headline'] and datas[data]['avatar_url']:
                user = User(username = data,about_me = datas[data]['headline'],avatar_hash = datas[data]['avatar_url'],location=u'腾讯大厦')
                user.confirmed = True
                user.password = '123'
                db.session.add(user)
                db.session.commit()
                if count == 100:
                    break

        print 'done'

    @staticmethod
    def create_qa():
        datas = json.load(open('G:/virtualenv/gaohu/gaohu/app/question_answers.json'))
        titles = json.load(open('G:/virtualenv/gaohu/gaohu/app/tmp.json'))
        count = 0
        for title in titles:
            for data in datas:
                count += 1
                if data[-16:-8] == title:
                    randx = random.randint(1,61)
                    u = User.query.filter_by(id=randx).first()
                    q = Question(body=titles[title],author=u)
                    db.session.add(q)
                    db.session.commit()
                    for answerdict in datas[data]:
                        y = random.randint(1,61)
                        user = User.query.filter_by(id=y).first()
                        a = Answer(body=datas[data][answerdict],author=user,Question_id=q.id)
                        db.session.add(a)
                        db.session.commit()
        print 'ok'

    def gravatar(self, size=100, default='identicon', rating='g'):
        x = randint(1,256)
        hashcode = "%s@gaopeng.com" % x
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar or hashlib.md5(
            hashcode).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
    @property
    def followed_posts(self):
        return Answer.query.join(Follow, Follow.followed_id == Answer.author_id)\
            .filter(Follow.follower_id == self.id)

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
