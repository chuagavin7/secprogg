

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from Product.models import Product
import logging
logger = logging.getLogger(__name__)

def index(request, page=1):
    products = Product.objects.all()

    if request.method == "GET" and 'search' in request.GET:
        print("waw")
        search = request.GET['search'].split(',')
        filterer = Q()

        for s in search:
            filterer = filterer | Q(name__icontains=s)

        products = products.filter(filterer)
    
    elif request.method == "GET" and 'sort' in request.GET:
        sort = request.GET['sort'].split(',')
        filterer = Q()

        for s in sort:
            filterer = filterer | Q(type__icontains=s)

        products = products.filter(filterer)
    
    context = {
        'products': products,
    }

    paginator = Paginator(products, 8)

    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page <= 0:
        page = 1

    products = paginator.page(page)
    context['products'] = products
    context['page'] = page
    return render(request, 'index.html', context)

def not_found(request):
    return render(request, 'errors/404.html')
 
def permission_denied(request):
    return render(request, 'errors/403.html')
 
def bad_request(request):
    return render(request, 'errors/400.html')

def server_error(request):
    return render(request, 'errors/500.html')