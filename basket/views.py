from urllib import response
from django.shortcuts import render ,get_object_or_404

from django.http import JsonResponse

from .basket import Basket
from store.models import Product 
# Create your views here.


def basket_summary(request):
    return render(request, "store/basket/summary.html")


def basket_add(request):
    basket =Basket(request)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        product = get_object_or_404(Product, id=product_id) 
        basket_qty = basket.__len__()
        basket.add(product=product, product_qty=product_qty)
        response = JsonResponse({'qty':basket_qty})
        return response
    