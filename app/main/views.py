from flask import render_template
from . import main
from ..models import Creativity,Project,User_atten_project
from flask_login import current_user

@main.route('/')
def index():
    creativityList = Creativity.query.order_by(Creativity.creativityId.desc()).limit(4).all()
    projectList = Project.query.order_by(Project.projectId.desc()).limit(4).all()
    dict_cre={}
    dict_pro={}
    for i in range(len(creativityList)):
        dict_cre['title'+str(i+1)] = creativityList[i].title
        if creativityList[i].type=='one':
            dict_cre['type' +str(i+1)] = 'software'
        else:
            dict_cre['type' +str(i+1)] = 'hardware'
        dict_cre['key'  +str(i+1)] = creativityList[i].key_word
        dict_cre['disc'+str(i+1)] = creativityList[i].describe

    for i in range(len(projectList)):
        dict_pro[str(i+1)] = projectList[i].projectId
        dict_pro['title'+str(i+1)] = projectList[i].title
        if projectList[i].type=='one':
            dict_pro['type'+str(i+1)] = 'software'
        else:
            dict_pro['type'+str(i+1)] = 'hardware'
        dict_pro['key'+str(i+1)] = projectList[i].key_word
        dict_pro['desc'+str(i+1)] = projectList[i].describe
    if current_user.is_authenticated:
        for i in range(len(projectList)):
            if User_atten_project.query.filter_by(userId=current_user.userId,
                                                  projectId=projectList[i].projectId).first():
                dict_pro['follow'+str(i+1)] = True

    return render_template('main/index.html',dict_cre = dict_cre,dict_pro=dict_pro)

@main.route('/about')
def about():
    return render_template('main/about.html')