import jwt
from models.UserModel import User  
from flask import request,g, jsonify
from sqlalchemy.orm import Session

class UsersController:
    # @staticmethod
    def get_user(db:Session):
        user= db.query(User).all()
        if not user:
            return jsonify({"message": "There are no users is empty"}), 404
        return jsonify([user.serialize() for user in user]), 200
    
    
    def getUserById(db:Session,user_id):
        user= db.query(User).where(User.user_id == user_id).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user.serialize()), 200
    