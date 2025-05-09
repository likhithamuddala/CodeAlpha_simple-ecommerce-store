from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Order, OrderItem
from .forms import CustomUserRegistrationForm


# Welcome Home Page
def home_view(request):
    return render(request, 'store/home.html')


# Product List View
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


# Add to Cart View
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Fix here: use .filter().first() instead of .get()
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    if not order:
        order = Order.objects.create(user=request.user, is_ordered=False)

    # Create or update OrderItem
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect('cart')


# Cart View
@login_required
def cart_view(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    items = order.items.all() if order else []
    total = order.get_total() if order else 0
    return render(request, 'store/cart.html', {'order': order, 'items': items, 'total': total})


# Checkout API
@csrf_exempt
@login_required
def checkout_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data.get('cart', {})

        order = Order.objects.filter(user=request.user, is_ordered=False).first()
        if not order:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            order_item, _ = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity = quantity
            order_item.save()

        order.is_ordered = True
        order.save()

        return JsonResponse({'status': 'success', 'order_id': order.id, 'total': order.get_total()})

    return JsonResponse({'error': 'Invalid method'}, status=400)


# Checkout Page
@login_required
def checkout_view(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    if not order or not order.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    total = order.get_total()

    if request.method == 'POST':
        order.is_ordered = True
        order.save()
        messages.success(request, f"Order placed successfully! Total: ₹{total}")
        return redirect('order_list')

    return render(request, 'store/checkout.html', {'order': order, 'total': total})


# Order List for User
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


# Profile
@login_required
def profile_view(request):
    return render(request, 'store/profile.html')


# Registration
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})


# API for Product List
def product_api(request):
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False)

# Remove item from the cart
@login_required
def remove_from_cart(request, product_id):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    if order:
        order_item = order.items.filter(product__id=product_id).first()
        if order_item:
            order_item.delete()
    return redirect('cart')
