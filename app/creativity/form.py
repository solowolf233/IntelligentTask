# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import Required,Length,EqualTo
from wtforms import ValidationError

class CreativityForm(Form):
    title = StringField(u'创意标题',validators=[Required(),Length(1,25)])
    type = SelectField(u'创意类型',validators=[Required()],choices=[('one','software'),('two','hardware')])
    key_word = StringField(u'关键字',validators=[Required(),Length(1,25)])
    describe = TextAreaField(u'创意描述',validators=[Required()])
    submit = SubmitField(u'提交')