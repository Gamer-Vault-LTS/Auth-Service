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