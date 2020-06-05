from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.userRegister, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('user/', views.userPage, name='user_page'),
    path('account/', views.accountSettings, name='account'),


    path('products/', views.products, name='products'),
    path('customer/<str:customer_id>/', views.customer, name='customer'),

    path('create_order/<str:customer_id>/', views.createOrder, name='create_order'),
    path('update_order/<str:order_id>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:order_id>/', views.deleteOrder, name='delete_order'),
    path('create_random_order/', views.createRandomOrder, name='create_random_order'), 

    #password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"),
        name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_form.html"),
        name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_done.html"),
        name='password_reset_complete'),
]   

"""
1. Submit email     PasswordResetView.as_view()
2. email sent success message   PasswordResetDoneView.as_view()
3. link to password reset form  PasswordResetConfirmView.as_view()
4. password successfully changed message    PasswordResetCompleteView.as_view()
"""