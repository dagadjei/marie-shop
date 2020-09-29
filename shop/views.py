from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin



def register_page(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account created for " + user)  
                return redirect('shop:login')
    
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user= authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop:home')
            else:
                messages.info(request, 'username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('shop:login')


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
    paginate_by = 10
    template_name = 'home-page.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


        
    
    
class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

@login_required
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
            messages.info(request, "Item Quantity Updated")
        else:
            order.items.add(order_item)
            messages.info(request, "Added to Cart")
            return redirect("shop:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Added to Cart") 
        return redirect("shop:order-summary")
    return redirect("shop:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("shop:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:product", slug=slug)
    
 

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:product", slug=slug)
    
 
   








