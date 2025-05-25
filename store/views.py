from django.shortcuts import render, get_object_or_404, redirect
from .models import Shoe, CartItem, Brand

def home(request):
    shoes = Shoe.objects.all()
    return render(request, 'store/home.html', {'shoes': shoes})

def product_detail(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    return render(request, 'store/product_detail.html', {'shoe': shoe})

def add_to_cart(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    cart = request.session.get('cart', {})
    cart[str(shoe_id)] = cart.get(str(shoe_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for shoe_id, quantity in cart.items():
        shoe = get_object_or_404(Shoe, id=shoe_id)
        total_price = shoe.price * quantity
        items.append({'shoe': shoe, 'quantity': quantity, 'total_price': total_price})
        total += total_price
    return render(request, 'store/cart.html', {'items': items, 'total': total})

def update_cart(request, item_id):
    cart = request.session.get('cart', {})
    shoe = get_object_or_404(Shoe, id=item_id)
    quantity = cart.get(str(item_id), 0)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase' and quantity < shoe.stock:
            cart[str(item_id)] = quantity + 1
        elif action == 'decrease' and quantity > 1:
            cart[str(item_id)] = quantity - 1
        request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for shoe_id, quantity in cart.items():
        shoe = get_object_or_404(Shoe, id=shoe_id)
        total_price = shoe.price * quantity
        items.append({'shoe': shoe, 'quantity': quantity, 'total_price': total_price})
        total += total_price
    return render(request, 'store/checkout.html', {'items': items, 'total': total})

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

def faq(request):
    return render(request, 'store/faq.html')

def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'store/terms_and_conditions.html')

def refund_policy(request):
    return render(request, 'store/refund_policy.html')

def warranty(request):
    return render(request, 'store/warranty.html')

def shop(request):
    shoes = Shoe.objects.all()
    brands = Brand.objects.all()

    # Filtering
    brand_id = request.GET.get('brand')
    if brand_id:
        shoes = shoes.filter(brand_id=brand_id)

    # Sorting
    price = request.GET.get('price')
    if price == 'low':
        shoes = shoes.order_by('price')
    elif price == 'high':
        shoes = shoes.order_by('-price')

    context = {
        'shoes': shoes,
        'brands': brands,
    }
    return render(request, 'store/shop.html', context)