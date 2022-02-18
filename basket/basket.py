

import basket


class Basket():
    """
    A base Basked class
    """

    def __init__(self, request):

        self.session = request.session 
        basket = self.session.get('skey')

        if 'skey' not in request.session:
            basket= self.session['skey'] = {}
        
        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding  and updating basket session data
        """

        product_id = product.id
        # ?? session got problem 
        if product_id not in self.basket:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty':product_qty,
            }
        else:
            self.basket[product_id]['qty'] = product_qty 
        
        self.session.modified = True

    def __len__(self):
        """
        Count qty of items
        """

        return sum( item['qty'] for item in self.basket.values())
