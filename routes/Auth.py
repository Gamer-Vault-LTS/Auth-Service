from datetime import date, datetime
from . import *
from controller.AuthController import AuthController
from utils.security import SecurityUserController

auth_route = Blueprint('auth',__name__)


sc = SecurityUserController()
auth = AuthController


@auth_route.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    return auth.login(data)


@auth_route.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    return auth.register(data)

@auth_route.route('/auth/changepassword', methods=['POST'])
def change_password():
    data = request.json
    return auth.change_password(data)

@auth_route.route('/auth/deactivateuser', methods=['POST'])
def deactivate_user():
    data = request.json 
    return auth.deactivate_user(data)

@auth_route.route('/auth/deleteuser', methods=['POST'])
def delete_user():
    data = request.json 
    return auth.delete_user(data)