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

#!!!!!!!
    # 注  在数据表中，只要是type   state   sex，数据类型都为Interge
#!!!!!!!
#:type的类型应该是Interger，但现在是String，迁移时应该改过来
# 1：个人  2：大学生   3：企业
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    email = db.Column(db.String(64),unique=True,nullable=False)
    username = db.Column(db.String(64),unique=True,nullable=False)
    tel = db.Column(db.Integer,unique=True)
    pwd = db.Column(db.String(128))
    confirmed = db.Column(db.BOOLEAN,default=False)
    type = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    nick = db.Column(db.String(64))
    wechat = db.Column(db.String(64))
    qq = db.Column(db.Integer)
    note = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    university = db.Column(db.String(64))
    enterprise = db.Column(db.String(64))
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
        db.session.commit()
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




#type的类型应该为Interger，但现在是String，迁移时应该进行修改
#1：软件   2：硬件
class Creativity(db.Model):
    __tablename__ = 'creativity'
    creativityId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.Integer)
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)

class User_atten_create(db.Model):
    __tablename__ = 'user_atten_create'
    Id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    creativityId = db.Column(db.Integer,db.ForeignKey('creativity.creativityId'))


#state 1:未审核，2:已审核，3：已采纳 4：未采纳 5:已生成项目
class Solution(db.Model):
    __tablename__ = 'solution'
    solutionId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    creativityId = db.Column(db.Integer,db.ForeignKey('creativity.creativityId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.Integer)
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)


class User_atten_project(db.Model):
    __tablename__ = 'user_atten_project'
    Id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    projectId = db.Column(db.Integer,db.ForeignKey('project.projectId'))
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))

#项目有什么状态呢？
#state 1:无人申请 2:[userA]申请负责 3：[userA]正在进行 4：[userA]已完成
class Project(db.Model):
    __tablename__ = 'project'
    projectId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    solutionId = db.Column(db.Integer,db.ForeignKey('solution.solutionId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.Integer)
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)

#1:u'Development',2:u'Designing',3:u'Tools',4:u'Unknown'
class Product(db.Model):
    __tablename__='product'
    productId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    solutionId = db.Column(db.Integer,db.ForeignKey('solution.solutionId'))
    title = db.Column(db.String(64))
    type = db.Column(db.Integer)
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
    type = db.Column(db.Integer)
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)


#1:审核中  2：已同意 3：拒绝
class Project_Apply(db.Model):
    __tablename__ = 'project_apply'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectId = db.Column(db.Integer, db.ForeignKey('project.projectId'))
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    state=db.Column(db.Integer)
    reasons=db.Column(db.String(64))#用户为什么选择加入该项目
    experience=db.Column(db.String(64))#项目经历
    note=db.Column(db.String(64))#自身能力及在该项目中可发挥什么作用


#以下为新建的表
#state为发布的任务的状态
#1:无人申请 2：已有人申请 3：正在进行 4：已完成
class Task1(db.Model):
    __tablename__='task1'
    taskId = db.Column(db.Integer,primary_key=True,autoincrement = True)
    userId = db.Column(db.Integer,db.ForeignKey('users.userId'))
    state = db.Column(db.Integer)
    title = db.Column(db.String(64))
    type = db.Column(db.Integer)
    key_word = db.Column(db.String(64))
    describe = db.Column(db.Text)

#state为申请状态
#1:审核中  2：已同意 3：拒绝
class Task_apply(db.Model):
    __tablename__='task_apply'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taskId = db.Column(db.Integer,db.ForeignKey('task1.taskId'))
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    state=db.Column(db.Integer)
    reasons=db.Column(db.String(64))#用户为什么选择加入该项目
    experience=db.Column(db.String(64))#项目经历
    note=db.Column(db.String(64))#自身能力及在该项目中可发挥什么作用