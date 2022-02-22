# Create your views here.

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from orders.models import Order


from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token
from orders.views import user_orders
from store.models import Product

def account_register(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()


            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    
    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)

        print("uid", uid)
    except(user.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()

        login(request,user)
        return redirect('account:dashboard')
    else:
        return render(request,'account/registration/activation_invalid.html')


@login_required
def dashboard(request):
    orders = user_orders(request)
    print(orders)
    return render(request, 'account/dashboard/dashboard.html', {'orders':orders} )


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)

    
    return render(request, 'account/dashboard/profile_edit.html',{'user_form':user_form} )


@login_required
def profile_delete(request):
    user = UserBase.objects.get(user_name = request.user)
    user.is_active = False
    user.save()
    logout(request)

    return redirect('account:delete_confirmation' )

@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'account/wishlist.html',{'products':products})


@login_required
def add_wishlist(request, id):
    product = get_object_or_404(Product,id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, "Removed " + product.title + "to your wishlist.", extra_tags='Add')  
        
        # extra_lag control text in wishlist button 
    
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + "to your wishlist.", extra_tags='Remove')

    return HttpResponseRedirect(request.META["HTTP_REFERER"])
    

