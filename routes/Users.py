
from . import *
from controller.UserController import UsersController
from utils.security import token_required
user_route = Blueprint('users',__name__) 

ucontroller = UsersController

@user_route.route("/users/all",methods=['GET'])
# @token_required
def getUsersEndpoint():
    return ucontroller.get_user(g.db)

@user_route.route("/users/<user_id>/",methods=['GET'])
# @token_required
def getUserByIdEndpoint(user_id):
    return ucontroller.getUserById(g.db,user_id)

@user_route.route("/users/getlevel",methods=['POST'])    
def getUserLevelEndpoint():
    data = request.json 
    return ucontroller.getUserLevel(data)
