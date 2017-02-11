# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField,HiddenField
from wtforms.validators import DataRequired,Length,EqualTo
from wtforms import ValidationError

class Task_applyForm(Form):
    TaskId = HiddenField()
    reasons=TextAreaField(u'申请理由',validators=[DataRequired()])
    experience=TextAreaField(u'项目经历')
    note=TextAreaField(u'备注')
    submit = SubmitField(u'申请')