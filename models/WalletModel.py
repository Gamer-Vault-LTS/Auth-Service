from . import *


class Wallet(Base):
    __tablename__ = 'wallet'

    wallet_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False)
    balance = Column(Numeric(10, 2), default=0.00)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    
    def serialize(self):
        
        return {
            "wallet_id": self.wallet_id,
            "user_id": self.user_id,
            "balance": self.balance,
            "created_at": self.created_at,
        }