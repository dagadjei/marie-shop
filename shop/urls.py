from django.urls import path
from .views import (
    item_list, checkout, product, HomeView,
 ItemDetailView, add_to_cart,remove_from_cart,
 register_page, login_page, logout_user,OrderSummaryView,
)

app_name = 'shop'
urlpatterns = [
  
    path('', HomeView.as_view(), name='homepage'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout', logout_user, name='logout'),
    path('checkout/', checkout, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view, name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')

]
