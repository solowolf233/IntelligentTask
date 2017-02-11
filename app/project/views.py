# -*- coding:utf-8 -*-
from . import project
from flask import render_template,request,json,redirect,url_for,flash
from flask_login import login_required,current_user
from ..models import User_atten_project,Project,Solution,Project_Apply,User,Task
from .. import db
from .form import User_ProjectForm

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
    #2：实现申请加入项目（即改变项目的状态）

    #3同意后，生成对应 的 我的task条目
    #在我的task条目中改变任务状态
    if request.form['type'] == u'software':
        type = 1
    else: type = 2
    projectItem = Project(userId=current_user.userId,solutionId=request.form['solutionId'],
                          title=request.form['title'],type=type,
                          key_word=request.form['key_word'],describe=request.form['describe'],
                          state=1)
    db.session.add(projectItem)
    solution = Solution.query.filter_by(solutionId=request.form['solutionId']).first()
    solution.state = 5
    db.session.commit()
    projectItem = Project.query.filter_by(userId=current_user.userId,solutionId=request.form['solutionId']).first()
    projectId = projectItem.projectId
    return redirect(url_for('project.project_detail',projectId=projectId))

@project.route('/project_detail',methods=['GET'])
@login_required
def project_detail():
    projectId = request.args.get('projectId')
    dict={}
    if projectId==None:
        solutionId = request.args.get('solutionId')
        if solutionId==None:
            return u'服务器出现错误，请谅解！'
        projectItem = db.session.query(Project.title,Project.key_word,Project.describe)\
            .join(Solution).filter_by(solutionId=solutionId).first()
        print projectItem[0]
        dict['title'] = projectItem[0]
        dict['key'] = projectItem[1]
        dict['desc'] = projectItem[2]

        return render_template('/project/project_detail.html',dict=dict)
    projectItem = Project.query.filter_by(projectId=projectId).first()
    dict['title'] = projectItem.title
    dict['key'] = projectItem.key_word
    dict['desc'] = projectItem.describe

    return render_template('/project/project_detail.html',dict=dict)

@project.route('/join_now',methods=['GET','POST'])
@login_required
def join_Now():
    user_ProjectForm = User_ProjectForm()
    projectId = request.args.get('projectId')
    if projectId != None:
        user_ProjectForm.projectId.data = projectId
    if user_ProjectForm.validate_on_submit():
        #得到要申请加入的项目
        project_corr=Project.query.filter_by(projectId=user_ProjectForm.projectId.data).first()
        #申请理由存入数据库
        projectItem = Project_Apply(userId=current_user.userId,
                                    projectId=user_ProjectForm.projectId.data,
                                    reasons = user_ProjectForm.reasons.data,
                                    experience = user_ProjectForm.experience.data,
                                    note = user_ProjectForm.note.data,
                                    #既然能申请，说明项目此时并没有确定由谁负责
                                    state=1
                                    )
        db.session.add(projectItem)
        db.session.commit()
        #如果项目状态是1，则需要改变项目状态，否则不需要
        if project_corr.state == 1:
            project_corr.state=2
            # db.session.add(project_corr)
            db.session.commit()
        flash(u'you have applied!')
        return redirect(url_for('auth.auth_taskApply'))
    return render_template('/project/join_Now_Project.html',form=user_ProjectForm)

#点击‘有人申请’后触发
@project.route('/list_new',methods=['GET'])
@login_required
def list_new():
    projectId = request.args.get('projectId')
    #已经拒绝的项目不必再查看
    projectApplyList = db.session.query(User.username,Project_Apply.Id,Project_Apply.reasons,
                                        Project_Apply.experience,Project.title,
                                        Project_Apply.note).join(Project_Apply).\
        join(Project).filter(Project_Apply.state != 3).filter(Project_Apply.projectId==projectId).limit(3).all()

    dict = {}
    for i in range(len(projectApplyList)):
        dict['user' + str(i + 1)] = projectApplyList[i][0]
        dict['id'+str(i+1)]  = projectApplyList[i][1]
        dict['reasons' + str(i + 1)] = projectApplyList[i][2]
        dict['experience' + str(i + 1)] = projectApplyList[i][3]
        dict['projectTitle' + str(i + 1)] = projectApplyList[i][4]
        dict['note' + str(i + 1)] = projectApplyList[i][5]
    return render_template('/project/list_new.html',dict=dict)

# 1代表正在申请中（这是申请理由存入数据库的初始值 说明我要申请的这个项目还并没有任何人负责他，也就是项目的所有人还没有同意任何人）
# 2代表我已经成功被同意负责项目
# 3代表我申请的项目被别人加入了 我已经没机会负责了，或者是我直接被拒绝了，反正都是没机会参与项目了
@project.route('/admit',methods=['GET','POST'])
@login_required
def admit():
    #项目所有者同意以后，需要更改的信息有
    #申请状态（我的变为2，其他的变为3）
    #项目状态变为3
    #同时生成我的任务
    applyId = request.args.get('applyId')
    myApply = Project_Apply.query.filter_by(Id = applyId).first()
    projectApplyList = Project_Apply.query.filter_by(projectId = myApply.projectId).all()
    for i in range(len(projectApplyList)):
        projectApplyList[i].state = 3

        # db.session.add(projectApplyList[i])
    myApply.state = 2
    project_corr=Project.query.filter_by(projectId = myApply.projectId).first()
    project_corr.state = 3
    task_corr=Task(userId=myApply.userId,
                   title=project_corr.title,
                   projectId=project_corr.projectId,
                   type=project_corr.type,
                   key_word=project_corr.key_word,
                   describe=project_corr.describe,
                   state = 1
                   )
    db.session.add(task_corr)
    db.session.commit()
    flash(u'you have make your project beginning!')
    return redirect(url_for('auth.auth_project'))##404

@project.route('/reject',methods=['GET'])
@login_required
def reject():
    #点击拒绝后需要更改的信息有
    #我的申请状态变为3（因为我没机会参与项目了）
    applyId = request.args.get('applyId')
    myApply = Project_Apply.query.filter_by(Id = applyId).first()
    myApply.state = 3
    db.session.commit()
    return redirect(url_for('project.list_new'))


@project.route('/project')
def project():
    projectList = db.session.query(Project.projectId,Project.title,Project.describe)\
            .join(User).filter(User.type == 2).all()
    dict = {}
    for i in range(len(projectList)):
        dict['projectId' + str(i + 1)] = projectList[i][0]
        dict['projectTitle' + str(i + 1)] = projectList[i][1]
        dict['describe' + str(i + 1)] = projectList[i][2]
    return render_template('/project/project.html',dict=dict)








