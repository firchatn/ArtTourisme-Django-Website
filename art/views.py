
from art.models import *
from art.forms import RegisterForm, RegisterFormUpdate, AddAddress
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#import stripe
import datetime


def index(request):
    products = Product.objects.select_related('vat').order_by('-id')[:5]
    categories = Category.objects.filter(parent_category_id=None)
    carousel = Photo.objects.all().order_by('-id')[:5]

    return render(request, 'index.html',
                  {'products': products, 'categories': categories, 'carousel': carousel})


def sign_in(request):
    form = RegisterForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
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

                if request.GET.get('next', False):
                    return redirect(request.GET['next'])
                else:
                    return redirect('commerce:root')
        else:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                    if request.GET.get('next', False):
                        return redirect(request.GET['next'])
                    else:
                        return redirect('commerce:root')
                else:
                    messages.add_message(request, messages.ERROR,
                                         'Votre compte a ete desactive, veuillez-contacter le service client.')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Les identifiants que vous avez saisis sont incorrects !')

    return render(request, 'signin.html', {
        'get': request.GET,
        'form': form
    })


def sign_out(request):
    logout(request)
    return redirect('commerce:root')


def display_category(request, category_id):
    """
    Cette fonction permet de visualiser les produits contenus dans une categorie.
    :type request:
    :param request:
    :param category_id: Id de la categorie a visualiser
    :return:
    """
    category = get_object_or_404(Category, pk=category_id)
    product_list = category.all_products()
    paginator = Paginator(product_list, 12)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'category': category, 'products': products})


def display_product(request, product_id):
    """
    Cette fonction permet de visualiser un produit.
    :type request:
    :param request:
    :param product_id: Id du produit a visualiser
    :return:
    """

    product = get_object_or_404(Product, pk=product_id)
    pictures = Photo.objects.filter(product__pk=product.id)

    return render(request, 'product.html', {'product': product, 'pictures': pictures})


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


def __create_order_from_database_cart(request):


    client = Client.objects.get(user_id=request.user.id)
    order = Order(status=Order.WAITING,
                  client_id=client.id,
                  shipping_address_id=request.session['shipping_address'],
                  invoicing_address_id=request.session['invoicing_address'],
                  order_date=datetime.datetime.now()
                  )
    order.save()

    cart = CartLine.objects.filter(client_id=client.id)
    for cart_line in cart:
        order_detail = OrderDetail(order_id=order.id,
                                   product_id=cart_line.product_id,
                                   qty=cart_line.quantity,
                                   product_unit_price=cart_line.product.price,
                                   vat=cart_line.product.vat.percent
                                   )
        order_detail.save()

    cart.delete()

    return order


def add_to_cart(request, product_id, qty):

    if not request.user.is_authenticated():
        if 'cart' not in request.session:
            cart = dict()
        else:
            cart = request.session['cart']

        if product_id in cart:
            cart[product_id] = int(cart[product_id]) + int(qty)
        else:
            cart[product_id] = qty

        request.session['cart'] = cart
    else:
        client = Client.objects.get(user_id=request.user.id)
        if CartLine.objects.filter(product_id=product_id, client_id=client.id).exists():
            cart_line = CartLine.objects.get(product_id=product_id, client_id=client.id)
            cart_line.quantity += int(qty)
        else:
            cart_line = CartLine(product_id=product_id, client_id=client.id, quantity=qty)
        cart_line.save()

    lien_panier = '<a style="margin-top:-7px" class="pull-right btn btn-default" href="' + '"><i class="fa fa-shopping-cart"></i> Voir le panier</a>'
    lien_dismit = '<button data-dismiss="alert" style="margin-top:-7px; margin-right:10px;" ' +\
                  'class="pull-right btn btn-default"><i class="fa fa-close"></i> Continuer mes achats</button>'
    messages.add_message(request, messages.SUCCESS,
                         'Le produit a ete correctement ajoute a votre panier. ' + lien_panier + lien_dismit
                         )
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('commerce:root')


def clear_cart(request):

    if not request.user.is_authenticated() and 'cart' in request.session:
        del request.session['cart']
    else:
        client = Client.objects.get(user_id=request.user.id)
        CartLine.objects.filter(client_id=client.id).delete()

    return redirect(request.META.get('HTTP_REFERER'))


def display_cart(request):
    total = 0
    if not request.user.is_authenticated():
        if 'cart' in request.session:
            cart = list()
            for product_id, quantity in request.session.get('cart').iteritems():
                cart_line = CartLine(product_id=product_id, quantity=quantity)
                total += cart_line.total()
                list.append(cart, cart_line)
        else:
            cart = None
    else:
        client = Client.objects.get(user_id=request.user.id)
        cart = CartLine.objects.filter(client_id=client.id)
        for cart_line in cart:
            total += cart_line.total()
    return render(request, 'cart.html', {'cart': cart, 'grand_total': total})


@login_required(login_url='/sign-in')
def shipping(request):
    client = Client.objects.get(user_id=request.user.id)
    addresses_list = Address.objects.filter(client_id=client.id)

    if request.method == 'POST' and request.POST['shipping_address'] and request.POST['invoicing_address']:
        request.session['shipping_address'] = int(request.POST['shipping_address'])
        request.session['invoicing_address'] = int(request.POST['invoicing_address'])

    if 'shipping_address' in request.session and 'invoicing_address' in request.session:
        shipping_address = request.session['shipping_address']
        invoicing_address = request.session['invoicing_address']
    else:
        shipping_address = 0
        invoicing_address = 0

    if request.GET.get('next', False):
        return redirect(request.GET['next'])
    else:
        return render(request, 'shipping.html', {'addresses': addresses_list,
                                                 'shipping_address': shipping_address,
                                                 'invoicing_address': invoicing_address})


@login_required(login_url='/sign-in')
def add_address(request):
    if request.method == 'POST':
        add_address_form = AddAddress(request.POST)

        if add_address_form.is_valid():
            client = Client.objects.get(user_id=request.user.id)
            address = add_address_form.save(commit=False)
            address.client_id = client.id
            address.save()
            if request.GET.get('next', False):
                return redirect(request.GET['next'])
            else:
                redirect('commerce:addresses')
    else:
        add_address_form = AddAddress()
    return render(request, 'add_address.html', {'add_address_form': add_address_form})




@login_required(login_url='/sign-in')
def confirmation(request):

    return render(request, 'confirmation.html')


@login_required(login_url='/sign-in')
def account(request):
    form = RegisterFormUpdate(instance=request.user)
    if request.method == 'POST':
        form = RegisterFormUpdate(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.add_message(request, messages.SUCCESS, "Vos informations ont ete correctement mises a jour.")
            return render(redirect('commerce:account'))
    return render(request, 'account.html', {'form': form})


@login_required(login_url='/sign-in')
def orders(request):
    client = Client.objects.get(user_id=request.user.id)
    return render(request, 'orders.html', {'orders': client.orders()})


@login_required(login_url='/sign-in')
def addresses(request):
    client = Client.objects.get(user_id=request.user.id)
    return render(request, 'addresses.html', {'addresses': client.addresses()})
