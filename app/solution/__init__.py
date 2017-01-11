from flask import Blueprint

solution = Blueprint('solution',__name__)

from . import views
