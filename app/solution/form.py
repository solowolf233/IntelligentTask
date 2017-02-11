# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import Required,Length,EqualTo
from wtforms import ValidationError

class SolutionForm(Form):
    title = StringField(u'方案标题',validators=[Required(),Length(1,25)])
    type = SelectField(u'方案类型',validators=[Required()],choices=[('1',u'software'),('2',u'hardware')])
    key_word = StringField(u'关键字',validators=[Required(),Length(1,25)])
    describe = TextAreaField(u'方案描述',validators=[Required()])
    submit = SubmitField(u'提交')