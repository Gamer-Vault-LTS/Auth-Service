
from . import *
from controller.UserController import UsersController
user_route = Blueprint('users',__name__) 

ucontroller = UsersController

@user_route.route("/users/all",methods=['GET'])
def getUsersEndpoint():
    return ucontroller.get_user(g.db)

@user_route.route("/users/<user_id>/",methods=['GET'])
def getUserByIdEndpoint(user_id):
    return ucontroller.getUserById(g.db,user_id)

@user_route.route("/users/<user_id>/level",methods=['POST'])    
def getUserLevelEndpoint(user_id):
    return ucontroller.getUserLevel(g.db,user_id)
