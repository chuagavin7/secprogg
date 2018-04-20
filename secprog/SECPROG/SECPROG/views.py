

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

import logging
logging.basicConfig(filename='loglog.log',format='%(levelname)-5s %(message)-5s %(asctime)-5s ',level=logging.DEBUG)


# Create your views here.
from Product.models import Product
import logging
logger = logging.getLogger(__name__)

def index(request, page=1):
    products = Product.objects.all()

    if request.method == "GET" and 'search' in request.GET:
        search = request.GET['search'].split(',')
        filterer = Q()

        for s in search:
            filterer = filterer | Q(name__icontains=s)

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

def handler404(request):
    response = render_to_response('errors/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('errors/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response