# -*- coding:utf-8 -*-

from . import task
from flask_login import login_required
from flask import request,json
from .. import db
from ..models import Task,Project


@task.route('/complete_task',methods=['GET'])
@login_required
def complete_task():
    taskId = request.args.get('taskId')
    #完成任务就是将task的state变为‘已完成’ 2
    #将project的state变为 '已完成' 3

    #下面这点查询太复杂，，应该试试不太复杂的
    #ajax的寻找节点

    #现在差的是
    #点击立即加入，提交表单存入数据库，改变项目状态，查看申请加入项目的人提交的表单  项目人同意后生成对应的我的任务，改变项目状态
    taskItem = Task.query.filter_by(taskId=taskId).first()
    print taskItem.state
    projectId = db.session.query(Project.projectId).join(Task).filter_by(taskId=taskId).first()
    print projectId[0]
    projectItem = Project.query.filter_by(projectId=projectId[0]).first()

    taskItem.state = 2
    projectItem.state = 4

    db.session.commit()

    return json.dumps({'success':True}),200,[('Content-Type','application/json;charset=utf-8')]