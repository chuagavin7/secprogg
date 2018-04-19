"""SECPROG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from SECPROG import views 
from User import views as user_views
from Product import views as prod_views
from django.conf.urls import handler404, handler500, handler403, handler400

urlpatterns = [
    path('session_security/', include('session_security.urls')),
    path('admin/', admin.site.urls),
    path('login_register/', user_views.login_register, name='login_register'),
    path('logout/', user_views.logout, name='logout'),
    path('cart/(?P<message>\s+)', prod_views.cart, name='cart'),
    path('detail/<int:productid>/', prod_views.detail, name='detail'),
    path('add_cart/', prod_views.add_cart, name='add_cart'),
    path('buy/', prod_views.buy, name='buy'),
    path('profile/', user_views.profile, name='profile'),
    path('change_password/', user_views.change_password, name='change_password'),
    path('history/', prod_views.history, name='history'),
    path('financial/', prod_views.financial, name='financial'),
    path('clear_cart/', prod_views.clear_cart, name='clear_cart'),
    path('add_account/', user_views.add_account, name='add_account'),
    path('add_product/', user_views.add_product, name='add_product'),
    path('edit/<int:id>/', user_views.edit, name='edit'),
    path('delete/<int:id>/', user_views.delete, name='delete'),
    path('<int:page>/', views.index, name='index_page'),
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.not_found
handler500 = views.server_error
handler403 = views.permission_denied
handler400 = views.bad_request