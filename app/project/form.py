# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField,HiddenField
from wtforms.validators import Required,Length,EqualTo
from wtforms import ValidationError

class User_ProjectForm(Form):
    projectId = HiddenField()
    reasons=TextAreaField(u'申请理由',validators=[Required()])
    experience=TextAreaField(u'项目经历')
    note=TextAreaField(u'备注')
    submit = SubmitField(u'申请')
