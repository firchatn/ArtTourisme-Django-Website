from django.shortcuts import render, redirect , get_object_or_404, redirect
from art.forms import RegisterForm, RegisterFormUpdate, AddAddress, LoginForm
from django.contrib.auth import authenticate, login, logout
from art.models import *

def index(request):
    products = Product.objects.select_related('vat').order_by('-id')[:8]
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    return render(request, 'index.html', {'form': form, 'form2' : form2, 'products' : products})

def __move_session_cart_to_database_cart(request, client_id):
    if 'cart' in request.session:
        for product_id, qty in request.session['cart'].iteritems():
            if CartLine.objects.filter(product_id=product_id, client_id=client_id).exists():
                cart_line = CartLine.objects.get(product_id=product_id, client_id=client_id)
                cart_line.quantity += int(qty)
            else:
                cart_line = CartLine(product_id=product_id, client_id=client_id, quantity=qty)
            cart_line.save()
        del request.session['cart']
    return

def error(request):
    return render(request, 'error.html')

def logout_view(request):
    logout(request)
    return redirect('art:index')

def produits_view(request):
    products = Product.objects.select_related('vat').order_by('-id')[:8]
    return render(request, 'produit.html', {'products': products})

def contact_view(request):
    return render(request, 'contact.html')

def tunisie_view(request):
    return render(request, 'tunisie.html')

def about_view(request):
    return render(request, 'about.html')

def event_view(request):
    return render(request, 'event.html')

def single_view(request, id):
    product = Product.objects.get(id=id)
    pictures = Photo.objects.filter(product__pk=product.id)
    return render(request, 'single.html', {'product': product, 'pictures': pictures})

def cat_view_tapis(request):
    cat = Category.objects.filter(name='tapis')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def cat_view_tapis(request):
    cat = Category.objects.filter(name='tapis')
    print(cat)
    product =Product.objects.filter(category=cat)
    print(product)
    return render(request, 'produit.html', {'product': product})

def cat_view_habits(request):
    cat = Category.objects.filter(name='habits')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def cat_view_poterie(request):
    cat = Category.objects.filter(name='poterie')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def cat_view_mosaique(request):
    cat = Category.objects.filter(name='mosaique')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def cat_view_bijoux(request):
    cat = Category.objects.filter(name='bijoux')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def cat_view_cuivre(request):
    cat = Category.objects.filter(name='cuivre')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def cat_view_ceramique(request):
    cat = Category.objects.filter(name='ceramique')
    product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product})

def produits_view(request):
    products = Product.objects.all()
    return render(request, 'produit.html', {'products': products})