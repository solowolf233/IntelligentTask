# -*- coding:utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import config
from datetime import timedelta

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message=u'请登录后再进行访问！'
login_manager.remember_cookie_duration=timedelta(minutes=30)



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #这个相当于执行了Config类中的静态方法
    config[config_name].init_app(app)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    #注册蓝本

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .creativity import creativity as creativity_blueprint
    app.register_blueprint(creativity_blueprint)

    from .product import product as product_blueprint
    app.register_blueprint(product_blueprint)

    from .project import project as project_blueprint
    app.register_blueprint(project_blueprint)

    from .solution import solution as solution_blueprint
    app.register_blueprint(solution_blueprint)

    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    from .captcha import captcha as captcha_blueprint
    app.register_blueprint(captcha_blueprint)

    return app