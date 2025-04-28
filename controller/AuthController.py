import jwt
from models.UserModel import User
from models.ShoppingCartModel import ShoppingCart
from models.WalletModel import Wallet   
from flask import request,g, jsonify
from datetime import date, datetime
from utils.security import SecurityUserController
sc = SecurityUserController()


class AuthController:
    
    def login(data):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = g.db.query(User).filter_by(username= username).first()
        
        if not user:
            return jsonify({"error": "Unregistered User"}), 401
        
        if user.is_active == False:
            return jsonify({"error": "This user is deactivated"}), 401
        
        validate = sc.verify_password(password,user.password_hash)
        
        if not validate or user.username != username:
            return jsonify({"error": "Registered password or unregistered user"}), 401
        else:
            token = sc.generar_token_authorizer(user.user_id)
            return jsonify({"token": token}), 200



    def register(data):
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        required = ['username', 'birth_date', 'email', 'password_hash']
        
        for field in required:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} required'}), 400
            
        today = date.today()
        age = today.year - datetime.strptime(data['birth_date'], '%Y-%m-%d').year
        
        if age < 18:
            return jsonify({'error': 'You must be at least 18 years old'}), 400 
        
        #  validar el hasheo de la contraseña (nvp)
        password_hash = sc.hash_password(data['password_hash'])
        data['password_hash'] = password_hash
        
        try:
            if g.db.query(User).filter_by(username=data['username']).first():
                return jsonify({'error': 'The username is already in use'}), 400
            
            if g.db.query(User).filter_by(email=data['email']).first():
                return jsonify({'error': 'The email is already registered'}), 400
            
            user = User(**data)
            g.db.add(user)
            g.db.commit()
            g.db.refresh(user)
            
            newCart = ShoppingCart(user_id=user.user_id, products=[])
            g.db.add(newCart)
            g.db.commit()
            
            newWallet = Wallet(user_id=user.user_id)
            g.db.add(newWallet)
            g.db.commit()
            
        except Exception as e:
            g.db.rollback()
            return jsonify({'error': str(e)}), 500
        
        return jsonify({'message': 'Registered successfully'}), 201
    
    def change_password(data):
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 401
        required = ['user_id', 'current_password', 'new_password', 'password_confirm']
        
        for field in required:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} required'}), 401
        
        user_id = data['user_id']
        current_password = data['current_password']
        new_password = data['new_password']
        password_confirm = data['password_confirm']

        user = g.db.query(User).filter_by(user_id=user_id).first()

        
        if not user:
            return jsonify({"error": "Unregistered User"}), 401
        
        if current_password == new_password:
            return jsonify({'error': 'New password cannot be the same as the current password'}), 401
        
        if new_password != password_confirm:
            return jsonify({'error': 'New passwords do not match'}), 401
        
        validate = sc.verify_password(current_password,user.password_hash)
        
        if not validate:
            return jsonify({"error": "The current password is incorrect"}), 401
      
        password_hash = sc.hash_password(new_password)
        
        user.password_hash = password_hash
        g.db.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    
    def deactivate_user(data):
        data = request.json
        user_id = data['user_id']
        
        if not user_id:
            return jsonify({'error': 'No user provided'}), 400
        
        user = g.db.query(User).filter_by(user_id=user_id).first()
        
        if not user:
            return jsonify({"error": "Unregistered User"}), 401
        
        user.is_active = False
        g.db.commit()
        
        return jsonify({'message': 'User deactivated successfully'}), 200
    
    def delete_user(data):
        data = request.json
        user_id = data['user_id']
        
        if not user_id:
            return jsonify({'error': 'No user provided'}), 400
        
        user = g.db.query(User).filter_by(user_id=user_id).first()
        
        if not user:
            return jsonify({"error": "Unregistered User"}), 401
        
        g.db.delete(user)
        g.db.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        