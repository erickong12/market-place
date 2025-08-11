from app.models.cart import CartItem


class CartRepository:
    def __init__(self, db):
        self.db = db

    def get_all_carts(self):
        return self.db.query().all()

    def get_cart_by_id(self, cart_id):
        return self.db.query().filter_by(id=cart_id).first()

    def create_cart(self, cart_data):
        new_cart = self.db.model(**cart_data)
        self.db.add(new_cart)
        self.db.commit()
        return new_cart

    def update_cart(self, cart, cart_data):
        for key, value in cart_data.items():
            setattr(cart, key, value)
        self.db.commit()
        return cart

    def clear_cart(self, buyer_id: str):
        self.db.query(CartItem).filter(CartItem.buyer_id == buyer_id).delete()