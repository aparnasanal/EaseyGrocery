from django.urls import path
from WebApp import views

urlpatterns = [
    path('home/', views.home_page, name='home'),
    path('our_products/', views.all_products, name='our_products'),
    path('filtered_products/<cat_name>/', views.filtered_products, name='filtered_products'),
    path('single_item/<int:product_id>/', views.single_item, name='single_item'),

    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('save_message/', views.save_message, name='save_message'),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('save_user/', views.save_user, name='save_user'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_items/<int:item_id>/', views.delete_items, name='delete_items'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_page, name='payment'),
]