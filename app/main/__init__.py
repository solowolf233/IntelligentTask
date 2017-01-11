from flask import Blueprint

main = Blueprint('main', __name__) #template_folder='folder'

from . import views