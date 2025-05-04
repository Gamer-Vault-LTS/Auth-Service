import jwt
from models.UserModel import User  
from models.ChallengeLevelModel import ChallengeLevels
from flask import request,g, jsonify
from sqlalchemy.orm import Session

class UsersController:
    # @staticmethod
    def get_user(db:Session):
        try:
            user= db.query(User).all()
            if not user:
                return jsonify({"error": "There are no users is empty"}), 404
            return jsonify([user.serialize() for user in user]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
    def getUserById(db:Session,user_id):
        
        try:
            
            user= db.query(User).where(User.user_id == user_id).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify(user.serialize()), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def getUserLevel(data):
        
        try:
            data = request.json
        
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            if not data["user_id"]:
                return jsonify({'error': 'No user id provided'}), 400
            
            print("recibi datos")
            user_id = data["user_id"]  
            
            user = g.db.query(User).filter_by(user_id=user_id).first()
            print("encontre usuario")
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            user_level = user.challenge_level_id    
            user_progress = user.challenge_progress
            
            response = {
                "user_level": user_level,
                "user_progress": user_progress
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        