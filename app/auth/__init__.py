from flask import Blueprint

auth = Blueprint('auth', __name__) #template_folder='folder'

from . import views, errors