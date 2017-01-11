# -*- coding:utf-8 -*-
from . import db
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from enum import Enum

class DBEnum(Enum):
    @classmethod
    def get_enum(cls):
        return [i for i in cls.process.values()]
class CreState(DBEnum):
    process = {'initial':'进度1','middle':'进度2','later':'进度3'}

class UserType(DBEnum):
    process = {'stu':'大学生','enterprise':'企业','person':'个人'}

class SoluState(DBEnum):
    process = {'initial':'进度1','middle':'进度2','later':'进度3'}

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    email = db.Column(db.String(64),unique=True,nullable=False)
    username = db.Column(db.String(64),unique=True,nullable=False)
    tel = db.Column(db.Integer,unique=True)
    pwd = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=False)
    type = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    nick = db.Column(db.String(64))
    wechat = db.Column(db.String(64))
    qq = db.Column(db.Integer)
    note = db.Column(db.String(64))
    sex = db.Column(db.String(2))
        ######################################
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.userId})
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.userId:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    #######################################
##########################
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.pwd = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pwd,password)
    ##########################
    def get_id(self):
        try:
            return str(self.userId)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return '<User %r>' % self.username





class Creativity(db.Model):
    __tablename__ = 'creativity'
    creativityId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)

class User_atten_create(db.Model):
    __tablename__ = 'user_atten_create'
    Id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    creativityId = db.Column(db.Integer,db.ForeignKey('creativity.creativityId'))


#state 1:未审核，2:已审核，3：已采纳 4：未采纳
class Solution(db.Model):
    __tablename__ = 'solution'
    solutionId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    creativityId = db.Column(db.Integer,db.ForeignKey('creativity.creativityId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)


class User_atten_project(db.Model):
    __tablename__ = 'user_atten_project'
    Id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    projectId = db.Column(db.Integer,db.ForeignKey('project.projectId'))
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))

#项目有什么状态呢？
#state 1:无人申请 2:[userA]申请负责 3：[userA]正在负责 4：[userA]已完成
class Project(db.Model):
    __tablename__ = 'project'
    projectId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    solutionId = db.Column(db.Integer,db.ForeignKey('solution.solutionId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)

class Product(db.Model):
    __tablename__='product'
    productId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    solutionId = db.Column(db.Integer,db.ForeignKey('solution.solutionId'))
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)

#state 1:进行中 2：已完成
class Task(db.Model):
    __tablename__ = 'task'
    taskId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    projectId = db.Column(db.Integer,db.ForeignKey('project.projectId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)
