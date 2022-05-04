from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout 

from django.contrib import messages 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.
from .models import*
from .forms import OrderForm, CreateUserForm, DeveloperForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account was created for ' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'base/register.html', context)


@unauthenticated_user
def loginPage(request):
        
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
                

    context = {}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url = 'login')
@admin_only
def home(request):
    orders = Order.objects.all()
    developers = Developer.objects.all()
    total_developers = developers.count()
    total_orders = orders.count()
    done = orders.filter(status='Done').count()
    processing = orders.filter(status='Processing').count()
    pending = orders.filter(status='Pending').count()
   
    context = {'orders':orders, 'developers':developers, 'total_orders':total_orders,'done':done, 'processing':processing, 'pending':pending  }
    return render(request, 'base/dashboard.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['developer'])
def userPage(request):
    orders = request.user.developer.order_set.all()

    total_orders = orders.count()
    done = orders.filter(status='Done').count()
    processing = orders.filter(status='Processing').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders':orders, 'total_orders':total_orders,
	'done':done, 'processing':processing,'pending':pending}
    return render(request, 'base/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['developer'])
def accountSettings(request):
	developer = request.user.developer
	form = DeveloperForm(instance=developer)

	if request.method == 'POST':
		form = DeveloperForm(request.POST, request.FILES,instance=developer)
		if form.is_valid():
			form.save()
       


	context = {'form':form}
	return render(request, 'base/account_settings.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def projects(request):
    projects=Project.objects.all()
    return render(request, 'base/projects.html', {'projects':projects})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def orders(request):
    orders=Order.objects.all()
    return render(request, 'base/orders.html', {'orders':orders})


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def developer(request,pk_test):
    developer = Developer.objects.get(id=pk_test)
    orders = developer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs 

    context = {'developer':developer, 'orders':orders, 'order_count':order_count,'myFilter':myFilter}
    
    
    return render(request, 'base/developer.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Developer, Order, fields=('project', 'status','priority', 'note'), extra=10 )
	developer = Developer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=developer)
	#form = OrderForm(initial={'developer':developer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=developer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'base/order_form.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'base/order_form.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'base/delete.html', context)


