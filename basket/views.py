from urllib import response
from django.shortcuts import render ,get_object_or_404

from django.http import JsonResponse

from .basket import Basket
from store.models import Product 
# Create your views here.


def basket_summary(request):
    basket = Basket(request)
    return render(request, "basket/summary.html",{'basket':basket})


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

def basket_delete(request):
    basket =Basket(request)

    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("product_id"))
        
        basket.delete(product_id=product_id)
        basketqty = basket.__len__()
        total_price_basket = basket.get_total_price()
        response = JsonResponse({'success':"Deleted" ,'qty':basketqty, 'subtotal': total_price_basket})
        return response

def basket_update(request):
    basket =Basket(request)
    print(request.POST)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        basket.update(product_id=product_id, product_qty=product_qty)

        basketqty = basket.__len__()
        total_price_basket = basket.get_total_price()

        response = JsonResponse({'success':"Updated", 'qty':basketqty, 'subtotal': total_price_basket})
        return response
    