from django.shortcuts import render, redirect
from main.models import Product, Category, ConfirmCode
from main.forms import ProductCreateForm, RegisterForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def test(request):
    data = {
        "title": 'Matrix -5',
        "Description": 'Lorem Ipsum',
        "price": 120
    }
    return render(request, 'test.html', context=data)


def index(request):
    print(request.user)
    products = Product.objects.all()
    data = {
        'product_list': products

    }
    return render(request, 'index.html', context=data)


def detail(request, id):
    product = Product.objects.get(id=id)
    data = {
        'product': product
    }
    return render(request, 'detail.html', context=data)


def search(request):
    word = request.GET.get('search', '')

    if request.GET.get('from_price', '') == '':
        from_price = 0
    else:
        from_price = int(request.GET.get('from_price'))
    if request.GET.get('to_price', '') == '':
        to_price = 1000000
    else:
        to_price = int(request.GET.get('to_price'))

    category_id = None
    try:
        category_id = int(request.GET.get('category_id'))
    except:
        pass
    category_id = request.GET.get('category_id')

    products = Product.objects.filter(title__contains=word,
                                      price__gte=from_price,
                                      price__lte=to_price)
    if category_id:
        products = products.filter(category_id=category_id)
    data = {
        'product_list': products,
        'categories': Category.objects.all()
    }
    return render(request, 'search.html', context=data)


@login_required(login_url='/login/')
def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'create.html', context={'form': form})
    context = {
        'form': ProductCreateForm()
    }
    return render(request, 'create.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    context = {}
    next_url = request.GET.get('next', '/')
    context['next'] = next_url
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            context['Ошибка'] = 'Пользователь не найден'

    return render(request, 'login.html', context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            return render(request, 'register.html',context={'form': form})
    elif request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', context={'form': form})

def confirm(request):
    code = request.GET.get('code', '')
    try:
        user = ConfirmCode.objects.get(code=code).user
        user.is_active = True
        user.save()
        context = {
            'message_type': 'success',
            'message': 'You are successfulle activated!!!'
        }
    except:
        context = {
            'message_type': 'danger',
            'message': 'SOMETHING WRONG WITH YOUR CODE!!!'
        }
    return render(request, 'message.html', context=context)