from django.shortcuts import render, redirect
from django.views import View
from .models import Products, Customers, Carts, Payment, OrderPlaced, Review
from .forms import UserCreationForm, CreateUserForm, CustomerProfileForm, ProductForm
from .utils import average_rating
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    return render(request, 'app/home.html', locals())

def about(request):
    return render(request, 'app/about.html', locals())

def categoryView(request, val):
    product = Products.objects.filter(category=val)
    title = Products.objects.filter(category=val).values('title')
    return render(request, 'app/category.html', locals())

@login_required
def ProductDetail(request, pk):
    product = Products.objects.get(pk=pk)
    # product = Products.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)
    if reviews:
        rating =average_rating([review.rating for review in reviews])
    print(reviews)

    if request.method == "GET":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm()
    return render(request, 'app/product-detail.html', locals())

@login_required
def review(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        product = Products.objects.get(id=prod_id)
        comment = request.GET.get('comment')
        rating = request.GET.get('rating')
        user = request.user
        Review(user=user, product=product, comment=comment, rating=rating).save()

        return redirect('product-detail', pk=prod_id)

@login_required
def CategoryTitle(request, val):
    product = Products.objects.filter(title=val)
    title = Products.objects.filter(category=product[0].category).values('title')
    return render(request, 'app/category.html', locals())


def registeration(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Register successfully!")
            return redirect('login')
        else:
            messages.warning(request, "Invalid Input data!")

    return render(request, 'app/customer-regis.html', {'form':form})

@login_required
def profile(request):
    form = CustomerProfileForm()
    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customers(user=user, name=name, locality=locality, state =state,
                           mobile=mobile, city=city, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Save Successfully!')
        else:
            messages.warning(request, 'Invalid Input Data!')
    return render(request, 'app/profile.html', locals())

@login_required
def address(request):
    add = Customers.objects.filter(user=request.user)
    return render (request, 'app/address.html', locals())

@login_required
def update(request, pk):
    add = Customers.objects.get(pk=pk)
    form = CustomerProfileForm(instance=add)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            add = Customers.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Profile Update Successfully!')
        else:
            messages.warning(request, 'Invalid Input Data!')
    return render(request, 'app/updateAddress.html', locals())

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Products.objects.get(id=product_id)
    Carts(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Carts.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 4000
    return render(request, 'app/addToCart.html', locals())

@login_required
def checkout_cart(request):
    user = request.user
    add = Customers.objects.filter(user=user)
    cart_items = Carts.objects.filter(user=user)
    amount = 0
    for p in cart_items:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 4000
    razoramount = int(totalamount * 100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data = {"amount": razoramount, "currency": "KZT", "receipt": "order_rcptid_12"}
    payment_response = client.order.create(data=data)
    print(payment_response)

    order_id = payment_response['id']
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
        )
        payment.save()
    return render(request, 'app/checkout.html', locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id= request.GET.get('cust_id')
    user = request.user

    customer = Customers.objects.get(id=cust_id)

    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Carts.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Carts.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Carts.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 4000
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Carts.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Carts.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 4000
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Carts.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Carts.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 4000
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)



def search(request):
    query = request.GET['search']
    product = Products.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html', locals())

