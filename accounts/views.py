from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
# Create your views here.
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm

def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_orders = orders.count()
	delivered = orders.filter(status="Delivered").count()
	pending = orders.filter(status="Pending").count()

	Context = {'orders': orders, 'customers': customers,
	 'total_orders':total_orders,   'delivered':delivered,
	'pending':pending 
	}

	return render(request, 'accounts/dashboard.html',Context)

def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs

	context = {
		'customer': customer,
		'orders': orders,
		'order_count': order_count,
		'myFilter': myFilter
	}
	return render(request, 'accounts/customer.html', context)

def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})

def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=10)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	# forms = OrderForm(initial={'customer':customer});
	if request.method == 'POST':
		# print("Printing Post: ",request.POST)
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {
		'formset':formset
	}
	return render(request, 'accounts/order_form.html',context)

def updateOrder(request, pk):
	 
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		# print("Printing Post: ",request.POST)
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {
		'form':form
	}
	return render(request, 'accounts/order_form.html',context)

def delete(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item': order}
	return render(request, 'accounts/delete.html', context)

def loginPage(request):
	context = {}
	return render(request, 'accounts/login.html', context)

def registerPage(request):
	form = UserCreationForm()
	if form.is_valid():
		form.save()
	context = {'form': form}
	return render(request, 'accounts/register.html', context)
