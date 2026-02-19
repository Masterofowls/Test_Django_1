from django.shortcuts import render, redirect, get_list_or_404
from .models import Product, PickupPoint, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, "./products.html", {"products" : products})
# Роль сотрудника   ФИО	                                Логин	            Пароль
# Администратор	    Никифорова Весения Николаевна	    94d5ous@gmail.com	uzWC67

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products')
    else: 
        form = UserCreationForm()
    return render(request, "register.html", {"form", form})

@login_required
def create_order(request, product_id, pickup_point_id):
    product = get_list_or_404(Product, id=product_id)
    pickupPoint = get_list_or_404(PickupPoint, id=pickup_point_id)
    # if not pickupPoint:
    #     return render(request, "error.html", {"message", "Невереный пункт выдачи"})
    order =  Order.objects.create(user = request.user, pickupPoint=pickupPoint)
    order.products.add(product)
    order.save()
    return redirect("order_list")


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order_list.html", {"orders": orders})
        