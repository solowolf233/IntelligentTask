from flask import Blueprint

captcha = Blueprint('captcha', __name__) #template_folder='folder'

from . import views