from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Category, Dish, Order, OrderItem, Cart, CartItem
from django.db import transaction
import secrets
from django.conf import settings

def get_user_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            status=False
        )
        return cart
    guest_token = request.COOKIES.get('guest_cart')
    if guest_token:
        cart = Cart.objects.filter(
            guest_token=guest_token,
            status=False
        ).first()

        if cart:
            return cart
    return None

def home(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()

    category_id = request.GET.get('category')
    spiciness = request.GET.get('spiciness')
    contains_walnuts = request.GET.get('contains_walnuts')
    is_vegetarian = request.GET.get('is_vegetarian')

    if category_id and category_id.isdigit():
        dishes = dishes.filter(category_id=int(category_id))

    if spiciness in ['0', '1', '2', '3', '4']:
        dishes = dishes.filter(spiciness=spiciness)
    if contains_walnuts in ['true', 'false']:
        dishes = dishes.filter(
            contains_walnuts=(contains_walnuts == 'true')
        )
    if is_vegetarian in ['true', 'false']:
        dishes = dishes.filter(
            is_vegetarian=(is_vegetarian == 'true')
        )
    return render(request, 'restaurant/home.html', {
        'categories': categories,
        'dishes': dishes,
        'category_id': category_id,
        'spiciness': spiciness,
        'contains_walnuts': contains_walnuts,
        'is_vegetarian': is_vegetarian,
    })




@require_POST
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = get_user_cart(request)

    if cart is None:
        guest_token = secrets.token_urlsafe(32)
        cart = Cart.objects.create(guest_token=guest_token)
    else:
        guest_token = None

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish
    )

    if not created:
        item.quantity += 1
        item.save()

    response = redirect('/#menu')

    if guest_token:
        response.set_cookie(
            'guest_cart',
            guest_token,
            max_age=2592000,
            httponly=True,
            samesite='Lax',
            secure=not settings.DEBUG
        )

    return response




def cart(request):
    user_cart = get_user_cart(request)
    cart_items = []
    total_price = 0

    if user_cart:
        items = CartItem.objects.filter(cart=user_cart).select_related('dish')

        for item in items:
            subtotal = item.dish.price * item.quantity
            total_price += subtotal

            cart_items.append({
                'dish': item.dish,
                'quantity': item.quantity,
                'subtotal': subtotal,
            })

    return render(request, 'restaurant/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@require_POST
def increase_quantity(request, dish_id):
    user_cart = get_user_cart(request)

    if user_cart:
        item = CartItem.objects.filter(
            cart=user_cart,
            dish_id=dish_id
        ).first()

        if item:
            item.quantity += 1
            item.save()

    return redirect('cart')



@require_POST
def decrease_quantity(request, dish_id):
    user_cart = get_user_cart(request)

    if user_cart:
        item = CartItem.objects.filter(
            cart=user_cart,
            dish_id=dish_id
        ).first()

        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

    return redirect('cart')



def checkout(request):
    user_cart = get_user_cart(request)

    if not user_cart:
        return redirect('cart')

    items = CartItem.objects.filter(cart=user_cart).select_related('dish')

    if not items.exists():
        return redirect('cart')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()

        if not customer_name or not phone_number or not address:
            return render(request, 'restaurant/checkout.html', {
                'error': 'გთხოვთ შეავსოთ ყველა ველი'
            })

        total_price = 0

        for item in items:
            total_price += item.dish.price * item.quantity

        with transaction.atomic():
            order = Order.objects.create(
                customer_name=customer_name,
                phone_number=phone_number,
                address=address,
                total_price=total_price
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    dish=item.dish,
                    quantity=item.quantity,
                    price=item.dish.price
                )

            items.delete()

        return redirect('order_success', order_id=order.id)

    return render(request, 'restaurant/checkout.html')

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'restaurant/order_success.html', {
        'order': order,
    })

