from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth') #todas las rutas con prefijo /auth seran roteadas a este blueprint

from . import views