
import bcrypt
class SecurityUserController:
    
    @staticmethod
    def hash_password(password:str):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt) 
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password_plain:str, password_hash:str):
        return bcrypt.checkpw(
            password_plain.encode('utf-8'),
            password_hash.encode('utf-8')
        )
