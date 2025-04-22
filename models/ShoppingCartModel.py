from . import *


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    
    cart_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    products = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    def serialize(self):
        return {
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "products": self.products,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
