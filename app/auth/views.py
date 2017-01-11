#/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_login import login_required,login_user,logout_user,current_user
from flask import render_template, request, session, redirect, url_for,flash
from datetime import datetime
from . import auth
from .forms import LoginForm,ProjectForm
from .forms import RegistrationForm
from .forms import UserInformationForm
from .. import db
from ..models import User,Creativity,Solution,Product,Task,Project
from ..email import send_email
from .. import login_manager




#个人信息保存
@auth.route('/auth/user_information',methods=['GET', 'POST'])
@login_required
def user_Information_Save():
    form = UserInformationForm()
    user = User.query.filter_by(userId=current_user.userId).first()
    if request.method== 'GET':
        form.username.data= user.username
        form.nick.data = user.nick
        form.sex.data = user.sex
        form.tel.data = user.tel
        form.wechat.data = user.wechat
        form.qq.data = user.qq
        form.note.data = user.note
    if form.validate_on_submit():
        user.username=form.username.data
        user.nick=form.nick.data
        user.sex=form.sex.data
        user.tel=form.tel.data
        user.wechat=form.wechat.data
        user.qq=form.qq.data
        user.note=form.note.data
        db.session.commit()
        flash(u'提交信息已保存！')
        return redirect(url_for('auth.user_Information_Save'))
    return render_template('auth/center/index.html',form=form)

@auth.route('/auth/creativity',methods=['GET','POST'])
@login_required
def auth_creativity():
    creativityList= Creativity.query.filter_by(userId=current_user.userId).limit(4).all()
    dict={}
    for i in range(len(creativityList)):
        dict['state'+ str(i+1)] = creativityList[i].state
        dict['title' + str(i+1)] = creativityList[i].title
        if creativityList[i].type=='one':
            dict['type' +str(i+1)] = 'software'
        else:
            dict['type' +str(i+1)] = 'hardware'
        dict['key'  +str(i+1)] = creativityList[i].key_word
        dict['desc'+ str(i+1)] = creativityList[i].describe

    return render_template('/auth/center/creative.html',dict=dict)

@auth.route('/auth/solution',methods=['GET','POST'])
@login_required
def auth_solution():
    #得到的我给别人所提出的方案
    solutionList = db.session.query(Solution.solutionId,Creativity.title,
                                    Solution.state,Solution.title,Solution.type,
                                    Solution.key_word,Solution.describe).join(Creativity).filter(
                                    Solution.userId == current_user.userId).all()
    dict={}
    stateDict={1:u'未查看',2:u'已查看',3:u'已采纳',4:u'未采纳'}
    for i in range(len(solutionList)):
        dict[str(i+1)] = solutionList[i][0]
        dict['cretitle'+str(i+1)] = solutionList[i][1]
        dict['state'+ str(i+1)] = stateDict[solutionList[i][2]]
        dict['solutitle'+str(i+1)] = solutionList[i][3]
        if solutionList[i][4]=='one':
            dict['type' +str(i+1)] = 'software'
        else:
            dict['type' +str(i+1)] = 'hardware'
        dict['key'+ str(i+1)] = solutionList[i][5]
        dict['desc'+ str(i+1)] = solutionList[i][6]

    return render_template('/auth/center/solution.html',dict=dict)

@auth.route('/auth/givensolution',methods=['GET','POST'])
@login_required
def auth_givensolution():
    #得到别人针对我的创意所给我提出的方案
    solutionList = db.session.query(Solution.solutionId,Creativity.title,
                                    Solution.state,Solution.title,Solution.type,
                                    Solution.key_word,Solution.describe).join(Creativity).filter(
                                    Creativity.userId == current_user.userId).all()
    dict={}
    stateDict={1:u'未查看',2:u'已查看',3:u'已采纳',4:u'未采纳'}
    #如果是已采纳，则后面再加一列，生成项目，，，，若不是，则没有这一列
    for i in range(len(solutionList)):
        dict[str(i+1)] = solutionList[i][0]
        dict['cretitle'+str(i+1)] = solutionList[i][1]
        dict['state'+ str(i+1)] = stateDict[solutionList[i][2]]
        dict['solutitle'+str(i+1)] = solutionList[i][3]
        if solutionList[i][4]=='one':
            dict['type' +str(i+1)] = 'software'
        else:
            dict['type' +str(i+1)] = 'hardware'
        dict['key'+ str(i+1)] = solutionList[i][5]
        dict['desc'+ str(i+1)] = solutionList[i][6]
    form = ProjectForm()
    return render_template('/auth/center/givensolution.html',dict=dict,form=form)

@auth.route('/auth/project',methods=['GET'])
@login_required
def auth_project():
    projectList = db.session.query(Project.projectId,Solution.title,
                                   Project.state,Project.title,
                                   Project.type,Project.key_word).join(Solution)\
                                  .filter(Project.userId == current_user.userId).all()
    dict={}
    stateDict={1:u'无人申请',2:u'有申请人',3:u'正在进行',4:u'已完成'}
    #在介绍申请人的界面中，如果选择申请人A，点击同意A以后，这个事情就算是成了
    for i in range(len(projectList)):
            dict[str(i+1)] = projectList[i][0]
            dict['solutitle'+str(i+1)] = projectList[i][1]
            dict['state' + str(i + 1)] =stateDict[projectList[i][2]]
            dict['protitle'+str(i+1)] = projectList[i][3]
            if projectList[i][4]=='one':
                dict['type' +str(i+1)] = 'software'
            else:
                dict['type' +str(i+1)] = 'hardware'
            dict['key'+str(i+1)] = projectList[i][5]
    return render_template('/auth/center/project.html',dict=dict)
@auth.route('/auth/product',methods=['GET','POST'])
@login_required
def auth_product():
    productList = Product.query.filter_by(userId=current_user.userId).limit(4).all()
    dict = {}
    for i in range(len(productList)):
        dict['solutionId'+str(i + 1)] = productList[i].solutionId
        print dict['solutionId'+str(i + 1)]
        dict['title' + str(i + 1)] = productList[i].title
        if productList[i].type == 'one':
            dict['type' + str(i + 1)] = 'software'
        else:
            dict['type' + str(i + 1)] = 'hardware'
        dict['key' + str(i + 1)] = productList[i].key_word
        dict['desc' + str(i + 1)] = productList[i].describe

    return render_template('/auth/center/product.html',dict=dict)

@auth.route('/auth/project_Item',methods=['GET','POST'])
@login_required
def auth_projectItem():
    return render_template('/auth/center/item.html')

@auth.route('/auth/taskModule',methods=['GET','POST'])
@login_required
def auth_taskModule():
    return render_template('/auth/center/taskModule.html')

@auth.route('/auth/task',methods=['GET','POST'])
@login_required
def auth_task():
    taskList = db.session.query(Task.state,Task.describe,Project.solutionId,Solution.creativityId).join(Project).join(Solution).all()
    dict = {}
    for i in range(len(taskList)):
        dict['prior' + str(i + 1)] = 'prior'
        dict['state' + str(i + 1)] = 'state'
        dict['creativityId' + str(i + 1)] = taskList[i].creativityId
        dict['solutionId' + str(i + 1)] = taskList[i].solutionId
        dict['taskModuleName' + str(i + 1)] = 'taskModuleName'
        dict['taskModuleDescribe' + str(i + 1)] = 'taskModuleDescribe'
        dict['captain' + str(i + 1)] = 'captain'
        dict['dueTime' + str(i + 1)] = 'dueTime'
        dict['desc' + str(i + 1)] = taskList[i].describe

    return render_template('/auth/center/task.html',dict=dict)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@auth.route('/test')
def test():
        template_txt = render_template('/auth/email/confirm.txt',token="token")
        template_html = render_template('/auth/email/confirm.html',token="token")
        r = send_email("ourren@outlook.com",template_txt,template_html)
        return str(r)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u"不匹配的账户密码.")
    return render_template('/auth/login.html',form=form)


@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,
                    password=form.password.data,date=datetime.now())
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)

        # flash(u'请前往您的注册邮箱进行验证:)')
        return redirect(url_for('.login'))

    return render_template('/auth/register.html', form=form)




@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()

    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#         and not current_user.confirmed \
#         and request.endpoint[:5] != 'auth.' \
#         and request.endpoint != 'static':
#         return redirect(url_for('auth.unconfirmed'))
# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')

