# -*- coding:utf-8 -*-
from flask_login import login_required,current_user
from flask import url_for,redirect,render_template,request,json
from . import creativity
from .. import db
from .form import CreativityForm
from ..models import Creativity,User_atten_create,Solution

@creativity.route('/creativity/attention',methods=['GET'])
@login_required
def attention():
    creativityId = int(request.args.get('creId'))
    u_a_c = User_atten_create.query.filter_by(userId=current_user.userId,creativityId=creativityId).first()
    if u_a_c is None:
        #说明要关注，添加进数据库
        u_a_c = User_atten_create(userId = current_user.userId,creativityId=creativityId)
        db.session.add(u_a_c)
        db.session.commit()
        return json.dumps({'success':True}),200,[('Content-Type','application/json;charset=utf-8')]
    else:
        #说明要取消关注，从数据库中删除该row
        db.session.delete(u_a_c)
        db.session.commit()
        return json.dumps({'success':True}),200,[('Content-Type','application/json;charset=utf-8')]

@creativity.route('/subCreativity',methods=['GET','POST'])
@login_required
def subCreativity():
    creativityForm = CreativityForm()
    if creativityForm.validate_on_submit():
        #先设定提交成功后跳转到创意集市界面
        creativityItem = Creativity(userId =current_user.userId,title = creativityForm.title.data
                                  ,type=creativityForm.type.data,key_word=creativityForm.key_word.data
                                    ,describe=creativityForm.describe.data)
        db.session.add(creativityItem)
        db.session.commit()
        return redirect(url_for('.creativity'))
    return render_template('creativity/subCreativity.html',form = creativityForm)

@creativity.route('/creativity',methods=['GET'])
def creativity():
    creativityList = Creativity.query.order_by(Creativity.creativityId.desc()).limit(12).all()
    dict = {}
    for i in range(len(creativityList)):
        dict[str(i+1)] = creativityList[i].creativityId
        dict['title'+str(i+1)] = creativityList[i].title
        if creativityList[i].type=='one':
            dict['type' +str(i+1)] = 'software'
        else:
            dict['type' +str(i+1)] = 'hardware'
        dict['key'  +str(i+1)] = creativityList[i].key_word
    if current_user.is_authenticated:
        for i in range(len(creativityList)):
            if User_atten_create.query.filter_by(userId=current_user.userId,
                                                 creativityId=creativityList[i].creativityId).first():
                dict['follow'+str(i+1)] = True
            if Solution.query.filter_by(userId=current_user.userId,
                                        creativityId=creativityList[i].creativityId).first():
                dict['solution'+str(i+1)]=True

    return render_template('creativity/creativity.html',dict=dict)









