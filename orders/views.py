from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from basket.basket import Basket

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)

    if request.method == "POST":
        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            # Order already built
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1 temporary placeholder',
                                address2='add2 temporary placeholder', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(key):
    pass
    Order.objects.filter(order_key=key).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
    