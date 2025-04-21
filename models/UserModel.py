from . import *

class User(Base):
    __tablename__ = "users"
    user_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(50), unique=True, nullable=True)
    password_hash = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    avatar = Column(String(255), nullable=True)
    
    def serialize(self):
        return {
        'user_id': self.user_id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'username': self.username,
        'email': self.email,
        "password_hash": self.password_hash,
        'phone': self.phone,
        'birth_date': self.birth_date,
        'created_at': self.created_at,
        'avatar': self.avatar
    }

