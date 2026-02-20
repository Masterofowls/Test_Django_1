from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from .models import Product, PickupPoint, Order, Profile
from .forms import SimplifiedUserCreationForm


def get_user_role(user):
    """Получить роль пользователя"""
    if not user.is_authenticated:
        return 'unauthorized'
    try:
        return user.profile.role
    except Profile.DoesNotExist:
        # Если профиль не существует, создаем его
        profile = Profile.objects.create(user=user, role='authorized')
        return profile.role


def require_role(allowed_roles):
    """Декоратор для проверки роли пользователя"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_role = get_user_role(request.user)
            if user_role not in allowed_roles:
                return HttpResponseForbidden("У вас нет прав доступа к этой странице")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def product_list(request):
    """Показать список товаров в зависимости от роли пользователя"""
    user_role = get_user_role(request.user)
    
    # Неавторизированный пользователь видит все товары без фильтрации
    products = Product.objects.all()
    
    # Авторизированный/Редактор/Админ могут видеть с фильтрацией
    if user_role in ['authorized', 'editor', 'admin']:
        search = request.GET.get('search', '')
        price_min = request.GET.get('price_min', '')
        price_max = request.GET.get('price_max', '')
        
        if search:
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
        if price_min:
            try:
                products = products.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                products = products.filter(price__lte=float(price_max))
            except ValueError:
                pass
    
    context = {
        'products': products,
        'user_role': user_role,
        'show_edit': user_role in ['editor', 'admin'],
        'show_delete': user_role == 'admin',
        'show_add_product': user_role == 'admin',
    }
    return render(request, 'products.html', context)


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = SimplifiedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Создаем профиль с ролью авторизированного пользователя
                # Проверяем, не существует ли уже профиль
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'authorized'}
                )
                if created:
                    print(f"✅ Профиль создан для пользователя {user.username}")
                else:
                    print(f"✅ Профиль уже существует для пользователя {user.username}")
                
                login(request, user)
                print(f"✅ Пользователь {user.username} успешно зарегистрирован и вошел в систему")
                return redirect('product_list')
            except Exception as e:
                print(f"❌ Ошибка при создании профиля: {e}")
                form.add_error(None, f"Ошибка при создании профиля: {str(e)}")
        else:
            print(f"❌ Ошибки валидации формы: {form.errors}")
    else:
        form = SimplifiedUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Вход в систему"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        print(f"🔐 Попытка входа: пользователь '{username}'")
        
        if not username or not password:
            error = 'Введите имя пользователя и пароль'
            print(f"❌ {error}")
            return render(request, 'login.html', {'error': error})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"✅ Пользователь {username} успешно вошел в систему")
            return redirect('product_list')
        else:
            error = 'Неверный логин или пароль'
            print(f"❌ {error} для пользователя '{username}'")
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('product_list')


@login_required(login_url='login')
@require_role(['authorized', 'editor', 'admin'])
def order_list(request):
    """Показать заказы пользователя"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})


@login_required(login_url='login')
@require_role(['authorized', 'editor', 'admin'])
def create_order(request, product_id, pickup_point_id):
    """Создать новый заказ"""
    product      = get_object_or_404(Product, id=product_id)
    pickup_point = get_object_or_404(PickupPoint, id=pickup_point_id)
    
    order = Order.objects.create(user=request.user, pickupPoint=pickup_point)
    order.products.add(product)
    
    return redirect('order_list')


@login_required(login_url='login')
@require_role(['editor', 'admin'])
def edit_product(request, product_id):
    """Редактировать товар"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.description = request.POST.get('description', product.description)
        product.sku = request.POST.get('sku', product.sku)
        product.save()
        return redirect('product_list')
    
    return render(request, 'edit_product.html', {'product': product})


@login_required(login_url='login')
@require_role(['admin'])
def delete_product(request, product_id):
    """Удалить товар"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    return render(request, 'confirm_delete.html', {'object': product, 'object_type': 'товара'})


@login_required(login_url='login')
@require_role(['admin'])
def add_product(request):
    """Добавить новый товар"""
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST.get('name', ''),
            price=request.POST.get('price', 0),
            description=request.POST.get('description', ''),
            sku=request.POST.get('sku', '')
        )
        return redirect('product_list')
    
    return render(request, 'add_product.html')


@login_required(login_url='login')
@require_role(['admin'])
def manage_users(request):
    """Управление пользователями (показ списка)"""
    from django.contrib.auth.models import User
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})


@login_required(login_url='login')
@require_role(['admin'])
def edit_user_role(request, user_id):
    """Изменить роль пользователя"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        profile.role = new_role
        profile.save()
        return redirect('manage_users')
    
    return render(request, 'edit_user_role.html', {'user': user, 'profile': profile})


@login_required(login_url='login')
@require_role(['admin'])
def delete_user(request, user_id):
    """Удалить пользователя"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=user_id)
    
    if request.user.id == user_id:
        return HttpResponseForbidden("Вы не можете удалить свой аккаунт")
    
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    
    return render(request, 'confirm_delete.html', {'object': user, 'object_type': 'пользователя'})
