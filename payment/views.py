
# Create your views here.



from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.basket import Basket
from orders.views import payment_confirmation
import os

@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    print(total)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    insent = stripe.PaymentIntent.create(
        amount=total,
        currency='eur',
        metadata={'userid': request.user.id}
    )

    return render(request,'payment/home.html', {'client_secret': insent.client_secret,
                                                'STRIPE_PUBLISHABLE_KEY':os.environ.get('STRIPE_PUBLISHABLE_KEY')})

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

