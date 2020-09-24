from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context)

def checkout(request):
    return render(request, 'checkout-page.html')


def product(request):
      
    return render(request, 'product-page.html')


class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check previous occurance of order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added to Cart")
        else:
            messages.info(request, "Added to Cart")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item) 
    return redirect("shop:product", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check previous occurance of order
        if order.items.filter(item__slug=item.slug).exists():
            order_item =  OrderItem.objects.filter(
                item=item, 
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
        else:
            #message to say no item as such exists
            return redirect("shop:product", slug=slug)
       
    else:
        #message to say no order
        return redirect("shop:product", slug=slug)

    return redirect("shop:product", slug=slug)








