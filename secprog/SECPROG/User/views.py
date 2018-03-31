from django.core import serializers
from django.shortcuts import render


# Create your views here.
from Product.models import Product
from User.models import User, Staff
from SECPROG.views import index


def login_register(request):
    context = {}
    if request.method == "POST":
        if 'login' in request.POST:
            try:
                user = User.objects.get(username=request.POST['username'], password=request.POST['password'])

                request.session['user'] = user.pk
                request.session['type'] = user.get_type()
                return index(request)

            except User.DoesNotExist:
                context['log_error'] = 'Cannot find an account with that combination.'
        elif 'register' in request.POST:
            try:
                user = User.objects.get(username=request.POST['username'])
                context['reg_error'] = 'That username is already taken.'
            except User.DoesNotExist:
                user = User(username=request.POST['username'], password=request.POST['password'], contact_num=request.POST['contact'],
                            name=request.POST['name'], billingAdd=request.POST['billing'], shippingAdd=request.POST['shipping'])
                user.save()
                context['reg_success'] = "Account has been created."

    return render(request, 'login.html', context)

def add_account(request):
    context = {}
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST['username'])

            context['reg_error'] = "Username is already taken."
        except:
            user = User(username=request.POST['username'], password=request.POST['password'], name=request.POST['password'])
            user.save()
            staff = Staff(user=user, type=int(request.POST['type']))

            staff.save()

            context['reg_success'] = "Account has been created."

    return render(request, 'add.html', context)


def add_product(request):
    context = {}

    if request.method == "POST":
        product = Product(name=request.POST['name'], type=int(request.POST['type']), quantity=request.POST['stock'],
                          description=request.POST['desc'], price=float(request.POST['price']), picture=request.FILES['picture'])
        product.save()

        context['add_log'] = "Product has been created"
    return render(request, 'add_product.html', context)


def delete(request, id):
    context = {}

    if id:
        try:
            product = Product.objects.get(id=int(id))
            product.delete()

            context['add_log'] = 'Product has been deleted'
        except Product.DoesNotExist:
            context['err_log'] = 'Cannot find the item to delete'

    return render(request, 'add_product.html', context)


def edit(request, id):
    context = {}

    if id:
        try:
            product = Product.objects.get(id=int(id))

            if request.method == "POST":
                product.name = request.POST['name']
                product.price = float(request.POST['price'])
                product.quantity = int(request.POST['stock'])
                product.description = request.POST['desc']
                product.type = int(request.POST['type'])

                if 'picture' in request.FILES:
                    product.picture = request.FILES['picture']

                product.save()
                context['edit_log'] = 'Product has been edited'

            context['product'] = product
            return render(request, 'edit.html', context)
        except Product.DoesNotExist:
            pass

    return index(request)

def logout(request):
    if 'user' in request.session:
        del request.session['user']
        del request.session['type']

    return index(request)


def profile(request):
    context = {}
    user = User.objects.get(id=request.session['user'])
    context['user'] = user
    return render(request, 'profile.html', context)

def change_password(request):
    context = {}

    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        old_pass = user.password

        if request.POST['pass'] == old_pass:
            user.password = request.POST['pass']
            user.save()

            context['change_success'] = "Password has been changed"
        else:
            context['change_error'] = "Incorrect old password."

    return render(request, 'profile.html', context)