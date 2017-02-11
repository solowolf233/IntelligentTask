from . import task1
from flask import render_template,request,json,redirect,url_for,flash
from flask_login import login_required,current_user
from .form import Task_applyForm
from ..models import User,Task1,Task_apply
from .. import db

#在任务界面中，用户B申请加入项目
@task1.route('/apply_join',methods=['GET','POST'])
@login_required
def apply_join():
    task_applyform = Task_applyForm()
    #这个参数在方法是GET 的时候就应该传过来
    taskId = request.args.get('taskId')
    if taskId != None:
        task_applyform.taskId.data = taskId
    if task_applyform.validate_on_submit():
        #得到要申请加入的task
        task=Task1.query.filter_by(taskId=task_applyform.taskId.data).first()
        #申请理由存入数据库
        task_apply = Task_apply(userId=current_user.userId,
                                    taskId=task_applyform.taskId.data,
                                    reasons = task_applyform.reasons.data,
                                    experience = task_applyform.experience.data,
                                    note = task_applyform.note.data,
                                    #既然能申请，说明项目此时并没有确定由谁负责
                                    state=1
                                    )
        db.session.add(task_apply)
        db.session.commit()
        #如果项目状态是1，则需要改变项目状态，否则不需要
        if task.state == 1:
            task.state=2
            # db.session.add(project_corr)
            db.session.commit()
        flash(u'you have applied!')
        return redirect(url_for())
    return render_template('',form=task_applyform)


#对于发布任务的人A来说，查看申请任务的用户
@task1.route('/list_new',methods=['GET'])
@login_required
def list_new():
    taskId = request.args.get('taskId')
    #已经拒绝的项目不必再查看
    taskApplyList = db.session.query(User.username,Task_apply.Id,Task_apply.reasons,
                                        Task_apply.experience,Task1.title,
                                        Task_apply.note).join(Task_apply).\
        join(Task1).filter(Task_apply.state != 3).filter(Task_apply.taskId==taskId).all()

    dict = {}
    for i in range(len(taskApplyList)):
        dict['user' + str(i + 1)] = taskApplyList[i][0]
        dict['id'+str(i+1)]  = taskApplyList[i][1]
        dict['reasons' + str(i + 1)] = taskApplyList[i][2]
        dict['experience' + str(i + 1)] = taskApplyList[i][3]
        dict['projectTitle' + str(i + 1)] = taskApplyList[i][4]
        dict['note' + str(i + 1)] = taskApplyList[i][5]
    return render_template('',dict=dict)

#任务所有者A同意以后，需要更改的信息有
#申请状态（同意的变为2，其他的变为3）
@task1.route('/admit',methods=['GET','POST'])
@login_required
def admit():
    applyId = request.args.get('applyId')
    myApply = Task_apply.query.filter_by(Id = applyId).first()
    taskApplyList = Task_apply.query.filter_by(taskId = myApply.taskId).all()
    for i in range(len(taskApplyList)):
        taskApplyList[i].state = 3

        # db.session.add(projectApplyList[i])
    myApply.state = 2
    db.session.commit()
    flash(u'you have make your Task beginning!')
    return redirect(url_for(''))

#拒绝某一个项目
#点击拒绝后需要更改的信息有
#拒绝的申请状态变为3（因为没机会参与任务了）
@task1.route('/reject',methods=['GET'])
@login_required
def reject():
    applyId = request.args.get('applyId')
    myApply = Task_apply.query.filter_by(Id = applyId).first()
    myApply.state = 3
    db.session.commit()
    return redirect(url_for(''))

