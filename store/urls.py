from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Homepage
    path('', views.home_view, name='store_home'),

    path('', views.home_view, name='home'),  # Home page URL
    path('cart/', views.cart_view, name='cart'),  # Cart page URL
    # Add other URLs here...

    # Product browsing
    path('products/', views.product_list_view, name='product_list'),
    path('api/products/', views.product_api, name='product_api'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # other URLs
    
    # Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    path('api/checkout/', views.checkout_api, name='checkout_api'),

    # Orders
    path('orders/', views.order_list, name='order_list'),

    # User profile
    path('profile/', views.profile_view, name='profile'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
