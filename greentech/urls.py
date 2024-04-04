"""greentech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin_index', admin_index, name="admin_index"),
    path('admin_login', admin_login, name="admin_login"),
    path('admin_profile', admin_profile, name="admin_profile"),
    path('user_profile', user_profile, name="user_profile"),
    path('admin_view_user', admin_view_user, name="admin_view_user"),
    path('delete_user/<int:pid>', admin_delete_user, name="delete_user"),
    path('delete_product/<int:pid>', admin_delete_product, name="delete_product"),
    path('admin_edit_product/<int:pid>', admin_edit_product, name="admin_edit_product"),
    path('admin_view_enquiry', admin_view_enquiry, name="admin_view_enquiry"),
path('view_feedback', view_feedback, name="view_feedback"),
    path('admin_view_product', admin_view_product, name="admin_view_product"),
    path('admin_view_order', admin_view_order, name="admin_view_order"),
    path('admin_add_product', admin_add_product, name="admin_add_product"),
    path('user_login', user_login, name="user_login"),
    path('new_address', new_address, name="new_address"),
    path('existing_address',existing_address,name="existing_address"),
    path('contact', contact, name="contact"),
    path('user_index', user_index, name="user_index"),
path('checkout/', checkout, name='checkout'),
    path('user_signup', user_signup, name="user_signup"),
    path('Logout', Logout, name="Logout"),
    path('swh', swh, name="swh"),
    path('on', on, name="on"),
    path('of', of, name="of"),
    path('ss', ss, name="ss"),
    path('sp', sp, name="sp"),
    path('baseswh', baseswh, name="baseswh"),
    path('baseon', baseon, name="baseon"),
    path('baseof', baseof, name="baseof"),
    path('basess', basess, name="basess"),
    path('basesp', basesp, name="basesp"),
    path('userswh', userswh, name="userswh"),
    path('useron', useron, name="useron"),
    path('userof', userof, name="userof"),
    path('userss', userss, name="userss"),
    path('usersp', usersp, name="usersp"),
    path('product-detail/<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('admin_product-detail/<int:pk>', AdminProductDetail.as_view(), name='admin-product-detail'),
    path('user_product-detail/<int:pk>', UserProductDetail.as_view(), name='user-product-detail'),
                  path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
                  path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
                  path('plus_cart/<int:cart_item_id>/', plus_cart, name='plus_cart'),
                  path('minus_cart/<int:cart_item_id>/', minus_cart, name='minus_cart'),
                  path('view_cart/', view_cart, name='view_cart'),
path('paymentdone', payment_done, name='paymentdone'),
path('orders/', orders, name='orders'),
path('change_status/<int:oid>', change_status, name='change_status'),
path('cancel_order/<int:oid>', cancel_order, name='cancel_order'),
path('download_invoice/<int:order_id>/', download_invoice, name='download_invoice'),
    path('add_feedback', add_feedback, name='add_feedback'),
    # path('generate_pdf', generate_pdf, name='generate_pdf'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
