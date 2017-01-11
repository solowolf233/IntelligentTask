# -*- coding:utf-8 -*-
from . import solution
from flask import url_for,redirect,render_template,request,json
from flask_login import login_required,current_user
from ..models import Solution
from .. import db
from .form import SolutionForm

@solution.route('/subSolution',methods=['GET','POST'])
@solution.route('/subSolution/<int:creId>',methods=['GET','POST'])
@login_required
def subSolution(creId):
    if creId==None:
        return render_template('creativity.creativity')
    solutionForm = SolutionForm()
    if solutionForm.validate_on_submit():
        solutionItem = Solution(userId =current_user.userId,creativityId=creId,title = solutionForm.title.data,key_word=solutionForm.key_word.data
                                  ,type=solutionForm.type.data,describe=solutionForm.describe.data)
        db.session.add(solutionItem)
        db.session.commit()
        return redirect(url_for('.solution'))
    return render_template('solution/subSolution.html',form = solutionForm,creId=creId)


@solution.route('/solution_detail',methods=['GET'])
def solution_detail():
    solutionId = request.args.get('solutionId')
    solution = Solution.query.filter_by(solutionId=solutionId).first()
    if solution is None:
        return "并无该方案，服务器可能出错了"
    if solution.state != 2:
        solution.state = 2
        db.session.commit()
    dict={}
    dict['title'] = solution.title
    dict['key'] = solution.key_word
    dict['desc'] = solution.describe

    return render_template('/solution/solution_detail.html',dict=dict)

@solution.route('/accept_solution',methods=['GET'])
@login_required
def accept_solution():
    #现在要采纳该方案，就是把solution的state变为3
    solutionId = request.args.get('solutionId')
    solution = Solution.query.filter_by(solutionId=solutionId).first()
    solution.state = 3
    db.session.commit()
    return redirect(url_for('auth.auth_givensolution'))

@solution.route('/reject_solution',methods=['GET'])
@login_required
def reject_solution():
    #现在要拒绝该方案，就是把solution的state变为4
    solutionId = request.args.get('solutionId')
    solution = Solution.query.filter_by(solutionId=solutionId).first()
    solution.state = 4
    db.session.commit()
    return redirect(url_for('auth.auth_givensolution'))

@solution.route('/solution',methods=['GET'])
def solution():
    solutionList = Solution.query.order_by(Solution.solutionId.desc()).limit(4).all()
    dict={}
    for i in range(len(solutionList)):
        dict[str(i+1)] = solutionList[i].solutionId
        dict['title'+str(i+1)] = solutionList[i].title
        if solutionList[i].type=='one':
            dict['type' +str(i+1)] = 'software'
        else:
            dict['type' +str(i+1)] = 'hardware'
        dict['key'  +str(i+1)] = solutionList[i].key_word
    return render_template('solution/solution.html',dict=dict)

