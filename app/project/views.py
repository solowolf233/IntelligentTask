# -*- coding:utf-8 -*-
from . import project
from flask import render_template,request,json
from flask_login import login_required,current_user
from ..models import User_atten_project
from .. import db

@project.route('/project/attention',methods=['GET'])
@login_required
def attention():
    projectId = request.args.get('proId')
    u_a_p = User_atten_project.query.filter_by(userId=current_user.userId,projectId=projectId).first()
    if u_a_p is None:
        #说明要关注，添加进数据库
        u_a_p = User_atten_project(userId = current_user.userId,projectId=projectId)
        db.session.add(u_a_p)
        db.session.commit()
        return json.dumps({'success':True}),200,[('Content-Type','application/json;charset=utf-8')]
    else:
        #说明要取消关注，从数据库中删除该row
        db.session.delete(u_a_p)
        db.session.commit()
        return json.dumps({'success':True}),200,[('Content-Type','application/json;charset=utf-8')]

@project.route('/create_project',methods=['GET','POST'])
@login_required
def create_project():
    #1：如何向modal中传递参数，，，，，
    #如何在提交表单时提交额外的参数，使用js

    #2：实现申请加入项目（即改变项目的状态）

    #3同意后，生成对应 的 我的task条目
    #在我的task条目中改变任务状态
    return render_template('/project/project_detail.html')

@project.route('/project_detail')
def project_detail():
    return render_template('/project/project_detail.html')

@project.route('/project')
def project():
    return render_template('/project/project.html')








