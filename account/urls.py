from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm

app_name = 'account'

urlpatterns = [
     path('register/', views.account_register, name='register'),
     path('activate/<slug:uidb64>/<slug:token>', views.account_activate, name='activate'),
     
     path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                  form_class=UserLoginForm), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
     
     # user details
     path('dashboard/', views.dashboard, name='dashboard'),

     path('profile/edit', views.profile_edit, name='profile_edit'),
     path('profile/delete_user', views.profile_delete, name='profile_delete'),
     path('profile/delete_confirm', TemplateView.as_view(
          template_name='account/dashboard/delete_confirm.html',), name='delete_confirmation'),

     path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/dashboard/password_reset_form.html",
                                                                      success_url='password_reset_email_confirm',
                                                                      email_template_name='account/dashboard/password_reset_email.html',
                                                                      form_class=PwdResetForm), name='pwdreset'),
     path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/dashboard/password_reset_confirm.html',
                                                                                                    success_url='password_reset_complete/',
                                                                                                    form_class=PwdResetConfirmForm),
          name="password_reset_confirm"),
     path('password_reset/password_reset_email_confirm/',
          TemplateView.as_view(template_name="account/dashboard/reset_status.html"), name='password_reset_done'),
     path('password_reset_confirm/NQ/password_reset_complete/',
         TemplateView.as_view(template_name="account/dashboard/reset_status.html"), name='password_reset_complete'),
     
     # wishlist
     path('wishlist/', views.wishlist, name='wishlist'), 
     path('wishlist/add/<int:id>', views.add_wishlist, name='add_wishlist'), 
]
