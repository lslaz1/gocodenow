from django.shortcuts import render, redirect
from django.http import HttpResponse
from ecomm.models import Product, Order, OrderProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):
	return render(request, 'index.html', {})

def signup(request):
	return render(request, 'signup.html', {})

def register(request):
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')
	email = request.POST.get('email')
	user = User.objects.create_user(first_name,last_name,email)
	return render(request, 'index.html', {})

def login(request):
	user = User.objects.all().last()
	return render(request, 'login.html', {})

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('shop/')
        else:
            return redirect('login/')
 
    else:
        # Return an 'invalid login' error message.
        pass

def item(request, prod_id):
	item = Product.objects.get(pk = prod_id)
	return render(request, 'item.html', {'item':item})

def shop(request):
	items = Product.objects.all()
	# print search
	if request.GET.get('search'):
		search = request.GET.get('search')
		items = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))

	
	if request.GET.get('filter') == '1':
		items = Product.objects.filter(price__lte=99.99)
		print items
	if request.GET.get('filter') == '2':
		items = Product.objects.filter(price__gte=100,price__lte=199.99)
	if request.GET.get('filter') == '3':
		items = Product.objects.filter(price__gte=200,price__lte=399.99)
	if request.GET.get('filter') == '4':
		items = Product.objects.filter(price__gte=400)


	if request.GET.get('format') == 'json':
		try:
			items = serializers.serialize('json', Product.objects.all())
			return HttpResponse(items, content_type='application/json') 
		except:
			return render(request, 'item.html', {'item_name':item.name,'item_description':item.description,'item_price':item.price})
		
	
	paginator = Paginator(items, 5)
	page = request.GET.get('page')
	try:
	    items = paginator.page(page)
	except PageNotAnInteger:
	    items = paginator.page(1)
	except EmptyPage:
	    items = paginator.page(paginator.num_pages)	
	return render(request, 'shop.html', {'all_items':items})

def cart(request):
	order = Order.objects.all().last()
	print "show cart",order.id
	# product = Product.objects.get(pk=prod_id)
	if order.status == 2:
		#create a new cart order object
		order = Order.objects.create(status=1)

	item_id = request.POST.get('item_id')
	quantity = 1

	#check to see if there is already a row tying a product to 
	#this order
	# op = OrderProduct.objects.get()order=order,product=product)
	# if op is not None:
		# order.quantity += 1
	#if so, update op.quantity

	#else carry on with the row below
	# else:
	op = OrderProduct(order=order,product_id=item_id, quantity = int(quantity))
	op.save()
	print "Adding to order",order.id,item_id

	products = order.product_set.all()
	return render(request, 'cart.html', {'products':products})

def show_cart(request):
	order = Order.objects.all().last()
	if order.status == 2:
		order = Order.objects.create(status=1)
	products = order.product_set.all()
	return render(request, 'cart.html', {'products':products})


	
def remove_item(request,prod_id):
	#get current order
	order = Order.objects.all().last()
	#get the product
	product = Product.objects.get(pk=prod_id)
	#find the OrderProduct row for this pair
	print "removeint from order",order.id,prod_id,product
	print order.product_set.all()
	op = OrderProduct.objects.get(order=order,product=product)
	#delete it, this is the reverse of line 60

	op.delete()
	# return render(request, 'cart.html', {'x.id':prod_id})
	return redirect('shop/cart/show/')

def checkout(request):
	order = Order.objects.all().last()
	order.status = 2
	order.save()
	return render(request, 'checkout.html', {})

def complete(request):
	return render(request, 'complete.html', {})












