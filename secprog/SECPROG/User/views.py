from django.core import serializers
from django.shortcuts import render
import re
# Create your views here.
from Product.models import Product
from User.models import User, Staff
from SECPROG.views import index
import hashlib 
import logging
from axes.utils import reset
from django.contrib.auth.signals import user_login_failed

logger = logging.getLogger(__name__)
def login_register(request):
    context = {}
    error = {}
    flag = 0
    if request.method == "POST":
        reg_error = []
        if 'login' in request.POST:
            try:
                password=request.POST['password']
                hashGen = hashlib.sha256()
                password = password.encode('utf-8')
                hashGen.update(password)
                hashed = hashGen.hexdigest()
                user = User.objects.get(username=request.POST['username'], password=hashed)
                request.session['user'] = user.pk
                request.session['type'] = user.get_type()
                logger.info('%s logged on the system at ', user.username)
                reset(username=request.user.username)
                return index(request)

            except User.DoesNotExist:
                username = request.user.username
                #inform axes of failed login
                user_login_failed.send(
                    sender = User,
                    request = request,
                    credentials = {
                        'username': username,
                    }
                )
                context['log_error'] = 'Cannot find an account with that combination.'
        elif 'register' in request.POST:
            try:
                user = User.objects.get(username=request.POST['username'])
                error['log_error'] =  'That username is already taken.'
            except User.DoesNotExist:
                password1 =request.POST['password1']
                password=request.POST['password']
                username=request.POST['username']
                contact_num=request.POST['contact']
                name=request.POST['name']
                name = name.split(' ')
                
                if username in ['11111111','12345678', 'abcd1234', 'account1', 'administrator', 'monkey123', 'username', 'qwertyuiop', 'test1234']:
                    context['reg_error'] = "Username too common!"
                    return render(request, 'login.html', context)
                    
                if password in ['12345678', '11111111', 'password', 'letmein1', 'administrator', 'account1', 'qwertyuiop', 'basketball', 'testtest']:
                    context['reg_error'] = "Password too common!"
                    return render(request, 'login.html', context)
                
                
                if password != password1:
                    context['reg_error'] = "Both entered passwords should match."
                    return render(request, 'login.html', context)
                elif password == password1:
                    if username == password:
                        context['reg_error'] = "Username and password should not match!"
                        return render(request, 'login.html', context)
                    
                    if re.match('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9#?!@$%^&*-]).{7,}$', password) and re.match('^[a-zA-Z0-9].{5,}$', username) and re.match('^(\+)(639)([0-9]{9})$', contact_num) and username.lower() not in password.lower():
                        for n in name:
                            if n in password:
                                flag += 1
                        if flag == 0:
                            hashGen = hashlib.sha256()
                            password = password.encode('utf-8')
                            hashGen.update(password)
                            hashed = hashGen.hexdigest()
                            user = User(username=request.POST['username'], password=hashed, contact_num=request.POST['contact'], name=request.POST['name'], billingAdd=request.POST['billing'], shippingAdd=request.POST['shipping'])
                            user.save()
                            context['reg_success'] = "Account has been created."
                    else:
                    
                        if re.match('^[a-zA-Z0-9].{5,}$', username) == None:
                            context['reg_error'] = "Username should only contain characters & numbers and should be least 6 characters long!"
                            return render(request, 'login.html', context)
                        if re.match('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9#?!@$%^&*-]).{7,}$', password) == None:
                            context['reg_error'] = "Password should contain both lower and upper case characters, one number & one symbol (#?!@$%^&*-) and should be at least 8 characters long!"
                            return render(request, 'login.html', context)
                        if flag > 0:
                            context['reg_error'] = "Password should not contain your name!"
                            return render(request, 'login.html', context)
                        if username.lower() in password.lower():
                            context['reg_error'] = "Password should not contain your username!"
                            return render(request, 'login.html', context)
                        if re.match('^(\+)(639)[0-9]{9}$', contact_num) == None:
                            context['reg_error'] = "Contact Number should be in the correct format!"
                            return render(request, 'login.html', context)

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
    flag = 0
    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        context['user'] = user
        username = user.username
        old_pass = user.password
        current_pass = request.POST['pass']
        hashGen = hashlib.sha256()
        current_pass = current_pass.encode('utf-8')
        hashGen.update(current_pass)
        hashedcurrent_pass = hashGen.hexdigest()
        if hashedcurrent_pass == old_pass:
            new_pass = request.POST['npass']
            name=user.name
            name=name.split(' ')
            if re.match('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9#?!@$%^&*-]).{7,}$', new_pass) and username.lower() not in new_pass.lower():
                for n in name:
                    if n.lower() in new_pass.lower():
                        flag += 1
                if flag == 0:
                    hashGen = hashlib.sha256()
                    new_pass = new_pass.encode('utf-8')
                    hashGen.update(new_pass)
                    hashednew_pass = hashGen.hexdigest()
                    user.password = hashednew_pass
                    user.save()
            else: 
                if re.match('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9#?!@$%^&*-]).{7,}$', new_pass) == None:
                    context['change_error'] = "Password should contain both lower and upper case characters, one number & one symbol (#?!@$%^&*-) and should be at least 8 characters long!"
                    return render(request, 'profile.html', context)
                if flag > 0:
                    context['change_error'] = "Password should not contain your name!"
                    return render(request, 'profile.html', context)
                if username.lower() in new_pass.lower():
                    context['change_error'] = "Password should not contain your username!"
                    return render(request, 'profile.html', context)
            context['change_success'] = "Password has been changed"
            
        else:
            context['change_error'] = "Incorrect old password."

    return render(request, 'profile.html', context)