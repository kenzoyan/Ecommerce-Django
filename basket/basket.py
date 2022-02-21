

from decimal import Decimal

from store.models import Product
from django.conf import settings

class Basket():
    """
    A base Basked class
    """

    def __init__(self, request):

        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)

        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}

        self.basket = basket

    def save(self):
        self.session.modified = True

    def add(self, product, product_qty):
        """
        Adding  and updating basket session data
        """

        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty': int(product_qty),
            }
        else:
            # += increase qty based on previous qty 
            self.basket[product_id]['qty'] += product_qty

        self.save()
        

    def __len__(self):
        """
        Count qty of items
        """

        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        """
        collect product id in session to get products in database
        """

        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            
            yield item

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        
        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(9.99)

        total = round(subtotal + Decimal(shipping),2)
        
        return total

    def delete(self, product_id):
        """
        Delete item in session data
        """
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product_id, product_qty):
        """
        Update item in session data
        """
        product_id = str(product_id)
   
        if product_id in self.basket:
            self.basket[product_id]['qty'] = int(product_qty)
        
        self.save()

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

