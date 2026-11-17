from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Category, Dish, Order, OrderItem
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm



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

    cart = request.session.get('cart', {})

    dish_id = str(dish.id)

    cart[dish_id] = cart.get(dish_id, 0) + 1

    request.session['cart'] = cart

    return redirect('/#menu')


def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for dish_id, quantity in cart_data.items():
        dish = Dish.objects.filter(id=dish_id).first()

        if dish:
            subtotal = dish.price * quantity
            total_price += subtotal

            cart_items.append({
                'dish': dish,
                'quantity': quantity,
                'subtotal': subtotal,
            })

    return render(request, 'restaurant/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@require_POST
def increase_quantity(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id = str(dish_id)

    if dish_id in cart:
        cart[dish_id] += 1
        request.session['cart'] = cart

    return redirect('cart')


@require_POST
def decrease_quantity(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id = str(dish_id)

    if dish_id in cart:
        if cart[dish_id] > 1:
            cart[dish_id] -= 1
        else:
            del cart[dish_id]

        request.session['cart'] = cart

    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
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
        order_items = []

        for dish_id, quantity in cart.items():
            dish = get_object_or_404(Dish, id=dish_id)

            if not isinstance(quantity, int) or quantity <= 0:
                return redirect('cart')

            subtotal = dish.price * quantity
            total_price += subtotal
            order_items.append((dish, quantity))

        with transaction.atomic():
            order = Order.objects.create(
                customer_name=customer_name,
                phone_number=phone_number,
                address=address,
                total_price=total_price,
            )

            for dish, quantity in order_items:
                OrderItem.objects.create(
                    order=order,
                    dish=dish,
                    quantity=quantity,
                    price=dish.price
                )
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)
    return render(request, 'restaurant/checkout.html')

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'restaurant/order_success.html', {
        'order': order,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'restaurant/register.html', {'form': form})