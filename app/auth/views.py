# -*- coding:utf-8 -*-
from datetime import datetime

from flask import render_template, request, redirect, url_for,flash,make_response,session
from flask_login import login_required,login_user,logout_user,current_user

from . import auth
from .forms import LoginForm,ProjectForm
from .forms import RegistrationForm
from .forms import UserInformationForm
from .. import db
from .. import login_manager
from ..email import send_email
from ..models import User,Creativity,Solution,Product,Task,Project,Project_Apply
from classes import ImageChar
import StringIO

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed\
            and request.endpoint != 'auth.confirm' and request.endpoint!= 'auth.logout':
        return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash()
    else:
        flash(u'The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()

    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash(u'A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


#个人信息保存
@auth.route('/auth/user_information',methods=['GET', 'POST'])
@login_required
def user_Information_Save():
    form = UserInformationForm()
    user = User.query.filter_by(userId=current_user.userId).first()
    if request.method== 'GET':
        form.username.data= user.username
        form.nick.data = user.nick
        form.sex.data = str(user.sex)
        form.tel.data = user.tel
        form.wechat.data = user.wechat
        form.qq.data = user.qq
        form.note.data = user.note
    if form.validate_on_submit():
        user.username=form.username.data
        user.nick=form.nick.data
        user.sex=int(form.sex.data)
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
    typeDict={1:u'software',2:u'hardware'}
    for i in range(len(creativityList)):
        dict[str(i+1)]=creativityList[i].creativityId
        dict['state'+ str(i+1)] = creativityList[i].state
        dict['title' + str(i+1)] = creativityList[i].title
        dict['type' +str(i+1)] = typeDict[creativityList[i].type]
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
    stateDict={1:u'未查看',2:u'已查看',3:u'已采纳',4:u'未采纳',5:u'已生成项目'}
    typeDict={1:u'software',2:u'hardware'}
    for i in range(len(solutionList)):
        dict[str(i+1)] = solutionList[i][0]
        dict['cretitle'+str(i+1)] = solutionList[i][1]
        dict['state'+ str(i+1)] = stateDict[solutionList[i][2]]
        dict['solutitle'+str(i+1)] = solutionList[i][3]
        dict['solutype'+str(i+1)] = typeDict[solutionList[i][4]]
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
    stateDict={1:u'未查看',2:u'已查看',3:u'已采纳',4:u'未采纳',5:u'已生成项目'}
    #如果是已采纳，则后面再加一列，生成项目，，，，若不是，则没有这一列
    typeDict={1:u'software',2:u'hardware'}
    for i in range(len(solutionList)):
        dict[str(i+1)] = solutionList[i][0]
        dict['cretitle'+str(i+1)] = solutionList[i][1]
        dict['state'+ str(i+1)] = stateDict[solutionList[i][2]]
        dict['solutitle'+str(i+1)] = solutionList[i][3]
        dict['solutype'+str(i+1)] = typeDict[solutionList[i][4]]
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
    typeDict={1:u'software',2:u'hardware'}
    #在介绍申请人的界面中，如果选择申请人A，点击同意A以后，这个事情就算是成了
    for i in range(len(projectList)):
            dict[str(i+1)] = projectList[i][0]
            dict['solutitle'+str(i+1)] = projectList[i][1]
            dict['state' + str(i + 1)] =stateDict[projectList[i][2]]
            dict['protitle'+str(i+1)] = projectList[i][3]
            dict['type' +str(i+1)] = typeDict[projectList[i][4]]
            dict['key'+str(i+1)] = projectList[i][5]
    return render_template('/auth/center/project.html',dict=dict)

@auth.route('/auth/product',methods=['GET','POST'])
@login_required
def auth_product():
    productList = Product.query.filter_by(userId=current_user.userId).limit(4).all()
    dict = {}
    typeDict={1:u'software',2:u'hardware'}
    for i in range(len(productList)):
        dict['solutionId'+str(i + 1)] = productList[i].solutionId
        dict['title' + str(i + 1)] = productList[i].title
        dict['type' + str(i + 1)] = typeDict[productList[i].type]
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


@auth.route('/auth/taskApply',methods=['GET'])
@login_required
def auth_taskApply():
    applyList = Project_Apply.query.filter_by(userId = current_user.userId).all()
    dict = {}
    stateList={1:u'审核中',2:u'同意负责（已生成任务)',3:u'已被拒绝'}
    for i in range(len(applyList)):
        dict['applyId'+str(i+1)] = applyList[i].Id
        dict['state' + str(i + 1)] = stateList[applyList[i].state]
        dict['proId'+str(i+1)] = applyList[i].projectId
    return render_template('/auth/center/taskApply.html',dict=dict)


@auth.route('/auth/task',methods=['GET','POST'])
@login_required
def auth_task():
    taskList = db.session.query(Task.taskId,Project.projectId,Task.state,Task.title).join(Project).all()
    dict = {}
    stateDict = {1:u'进行中',2:u'已完成'}
    for i in range(len(taskList)):
        dict[str(i+1)] = taskList[i][0]
        dict['proId'+str(i+1)] = taskList[i][1]
        dict['state' + str(i + 1)] = stateDict[taskList[i][2]]
        dict['title' + str(i + 1)] =taskList[i][3]

    return render_template('/auth/center/task.html',dict=dict)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@auth.route('/validateCode',methods=['GET'])
def get_code():
    imgChar = ImageChar()
    code_img,strs = imgChar.randImage(4)
    buf = StringIO.StringIO()
    code_img.save(buf,'JPEG',quality=70)
    buf_str = buf.getvalue()
    session['code_text'] = strs
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires']=0
    return response

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit() and session['code_text'] == form.verification.data:
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u"不匹配的账户密码.")
    if session['code_text'] != form.verification.data and request.method =='POST':
        code_error = u'验证码错误！'
    else:
        code_error = ''
    response = make_response(render_template('/auth/login.html',form=form,code_error=code_error))
    return response



@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if request.method=='GET':
        #生成验证码
        # imgChar = ImageChar()

        RegistrationForm.code_text = 'NHEV'
        print RegistrationForm.code_text
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,
                    password=form.password.data,date=datetime.now())
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('/auth/register.html', form=form,code_img='rand.jpg')





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

