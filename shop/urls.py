from django.urls import path
from .views import item_list, checkout, product

app_name = 'shop'
urlpatterns = [
    path('', item_list, name='item-list'),
    path('checkout/', checkout, name='checkout'),
    path('product/', product, name='product'),
]
