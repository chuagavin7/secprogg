from django.shortcuts import render

# Create your views here.
from Product.models import Product, Transaction
from SECPROG.views import index
from User.models import User
from .models import Review


def add_cart(request):
    if request.method == "GET":
        item = {}
        num = abs(int(request.GET['num']))
        item['num'] = num
        item['id'] = int(request.GET['id'])

        if 'cart' in request.session:
            request.session['cart'].append(item)
        else:
            request.session['cart'] = [item]

    return cart(request)


def cart(request):
    context = {
        'total': 0.0, 'num': 0
    }
    user = User.objects.get(id=request.session['user'])
    context['user'] = user
    products = []

    if 'cart' in request.session:
        for item in request.session['cart']:
            prod = {}
            try:
                product = Product.objects.get(id=item['id'])
                prod['total'] = product.price * item['num']
                prod['quantity'] = item['num']
                prod['product'] = product

                products.append(prod)
                context['total'] += prod['total']
                context['num'] += 1
            except Product.DoesNotExist:
                pass

    context['products'] = products
    return render(request, 'cart.html', context)

def detail(request, productid):
    product = Product.objects.get(id=int(productid))
    review = Review.objects.all()

    context = {"product": product, "review": review}
    
    return render(request, 'detail.html', context)


def history(request):
    context = {}

    products = []
    transactions = Transaction.objects.filter(user=request.session['user'])

    for t in transactions:
        prod = {}
        try:
            prod['total'] = t.product.price * t.quantity
            prod['quantity'] = t.quantity
            prod['product'] = t.product

            products.append(prod)
        except Product.DoesNotExist:
            pass

    context['products'] = products
    return render(request, 'history.html', context)

def financial(request):
    context = {
        'total': 0.0
    }
    product = Product.objects.all()
    transactions = Transaction.objects.all()
    money = 0
    analogT = 0
    smartT = 0
    digitalT = 0
    products = []
    products_filtered = []
    request.session['type_of'] = 3
    if request.GET and ('type_of' in request.session or 'type_of' in request.get):

        if request.session['type_of'] != int(request.GET.get('type_of', 3)):
            request.session['type_of'] = int(request.GET.get('type_of', 3))
        
    if 'type_of' in request.session:
        m = request.session['type_of']
    else: 
        m = 3
    
    for t in transactions:
        try:
            money += t.product.price * t.quantity

        except Product.DoesNotExist:
            pass
    
    for r in product:
        tempProduct = {}
        tempProduct['name'] = r.name
        tempProduct['total'] = 0
        tempProduct['quantity'] = 0
        tempProduct['price'] = r.price
        tempProduct['type_of'] = r.type
        tempProduct['type'] = r.string_type
        products.append(tempProduct)
    
    for t in transactions:
        for p in products:
            try:
                if p['name'] == t.product.name:
                    p['total'] += t.product.price * t.quantity
                    p['quantity'] += t.quantity
                    if p['type_of'] == 0:
                        analogT += t.product.price * t.quantity
                    elif p['type_of'] == 2:
                        smartT += t.product.price * t.quantity
                    elif p['type_of'] == 1:
                        digitalT += t.product.price * t.quantity
            except Product.DoesNotExist:
                pass
    if m == 3 or m == 4:
        context['products'] = products
    elif m == 0:
        for p in products:
            if p['type_of'] == 0:
                products_filtered.append(p)
            context['products'] = products_filtered
    elif m == 1:
        for p in products:
            if p['type_of'] == 1:
                products_filtered.append(p)
        context['products'] = products_filtered
    elif m == 2:
        for p in products:
            if p['type_of'] == 2:
                products_filtered.append(p)
        context['products'] = products_filtered
        
        
    context['money'] = money
    context['analogT'] = analogT
    context['digitalT'] = digitalT
    context['smartT'] = smartT
    return render(request, 'financial.html', context)

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']

    return cart(request)

def buy(request):
    if request.method == "POST":
        if 'cart' in request.session:
            for item in request.session['cart']:
                try:
                    product = Product.objects.get(id=item['id'])
                    user = User.objects.get(id=request.session['user'])
                    transaction = Transaction(product=product, user=user, quantity=item['num'], credit_card=request.POST['credit'])
                    transaction.save()
                except Product.DoesNotExist and User.DoesNotExist:
                    pass

    return clear_cart(request)