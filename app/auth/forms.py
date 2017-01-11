#/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField,RadioField,IntegerField,SelectField,DateField,TextAreaField,HiddenField

from wtforms.validators import Required,Length,Email,Regexp, EqualTo,DataRequired
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField(u'邮箱',validators=[DataRequired(),Length(1,64),Email(message=u"错误的邮箱格式.")])

    # username = StringField("what's your username?",validators=[Required()])
    password = PasswordField(u'密码',validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')

class RegistrationForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6, 12,message=u'密码长度在6到12位.'),EqualTo('password2', message=u'密码必须一致.')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired(),Length(6, 12,message=u'密码长度在6到12位.')])
    submit = SubmitField(u'Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册过.')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被占用.')


class UserInformationForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(message=u'不能为空'),Length(1,64)])
    nick = StringField(u'昵称', validators=[Length(1,64)])
    sex = RadioField(u'性别', choices =[('1',u'man'), ('2',u'woman'),('3',u'secret')])
    tel = StringField(u'手机号',validators=[Length(11)])
    wechat = StringField(u'微信号',validators=[Length(1,64)])
    qq = StringField(u'QQ',validators=[Length(5,12)])
    note= StringField(u'备注',validators=[Length(1,64)])
    submit = SubmitField(u'save')


class ProjectForm(Form):
    solutionId = HiddenField()
    title = StringField(u'标题',validators=[DataRequired(message=u'不能为空'),Length(1,64)])
    type = SelectField(u'类型',choices=[('1',u'software'),('2',u'hardware')],validators=[DataRequired(message=u'不能为空')])
    key_word = StringField(u'关键字',validators=[DataRequired(message=u'不能为空'),Length(1,64)])
    describe = TextAreaField(u'描述',validators=[DataRequired(message=u'不能为空'),Length(1,200)])
    submit = SubmitField(u'提交')


