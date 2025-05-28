from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProductForm, FeedbackForm, RegisterForm
from .models import Product, Category, Tag, Feedback

def get_base_menu(request):
    menu = [
        {"link": "/", "text": "Главная"},
        {"link": "/products/", "text": "Товары"},
        {"link": "/about/", "text": "О магазине"},
    ]
    if request.user.is_authenticated:
        menu.extend([
            {"link": "/profile/", "text": "Профиль"},
            {"link": "/logout/", "text": "Выйти"},
        ])
    else:
        menu.extend([
            {"link": "/login/", "text": "Войти"},
            {"link": "/register/", "text": "Регистрация"},
        ])
    return menu

def index_page(request):
    context = {
        "page_name": "Главная",
        "menu_items": get_base_menu(request),
    }
    return render(request, "index.html", context)

def about_page(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            return redirect('about')
    else:
        form = FeedbackForm()
    
    context = {
        "page_name": "О магазине",
        "menu_items": get_base_menu(request),
        "form": form,
        "feedbacks": Feedback.objects.all().order_by('-created_at')[:5],
    }
    return render(request, "about.html", context)

def products_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    
    if category_id:
        products = products.filter(category__id=category_id)
    if tag_id:
        products = products.filter(tags__id=tag_id)
    
    context = {
        "page_name": "Товары",
        "menu_items": get_base_menu(request),
        "products": products,
        "categories": categories,
        "tags": tags,
        "selected_category": int(category_id) if category_id else None,
        "selected_tag": int(tag_id) if tag_id else None,
    }
    return render(request, "products.html", context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    
    context = {
        "page_name": "Добавить товар",
        "menu_items": get_base_menu(request),
        "form": form,
    }
    return render(request, "add_product.html", context)

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    
    context = {
        "page_name": "Регистрация",
        "menu_items": get_base_menu(request),
        "form": form,
    }
    return render(request, "registration/register.html", context)

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    
    context = {
        "page_name": "Вход",
        "menu_items": get_base_menu(request),
        "form": form,
    }
    return render(request, "registration/login.html", context)

@login_required
def logout_page(request):
    logout(request)
    return redirect('index')

@login_required
def profile_page(request):
    context = {
        "page_name": "Профиль",
        "menu_items": get_base_menu(request),
        "user": request.user,
    }
    return render(request, "registration/profile.html", context)