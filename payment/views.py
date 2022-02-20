
# Create your views here.



import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.basket import Basket
from orders.views import payment_confirmation


@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    print(total)
    stripe.api_key = 'sk_test_51KVIHKHTQ3PmkJesXgGdeaqeTI531kPc6JyIwnAt58uvYegR42GGtyntSv3p5zM0LrO1NPZAZyvau47wyc62MXvy00P5y5C86c'

    insent = stripe.PaymentIntent.create(
        amount=total,
        currency='eur',
        metadata={'userid': request.user.id}
    )

    return render(request,'payment/home.html', {'client_secret': insent.client_secret})

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

