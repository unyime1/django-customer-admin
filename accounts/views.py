from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory #a way for us to create multiple forms within one form
#from django.contrib.auth.forms import UserCreationForm #nolonger necessary i think
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import * # one dot(.) means the same folder
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_users, allowed_users, admin_only
 


@login_required(login_url='login')
#@admin_only
@allowed_users(allowed_roles=['customer', 'admin'])
def home(request):
    """this function handles the home view"""

    #database queries
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count() 
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    shipped = orders.filter(status='Shipped').count()

    context = {'orders': orders, 'customers': customers,
    'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'shipped': shipped }
    return render(request, 'accounts/dashboard.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    """this function handles the user profile page containing user orders"""

    #database queries
    orders = request.user.customer.order_set.all() #request the orders of a logged in customer
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    shipped = orders.filter(status='Shipped').count()

    context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'shipped': shipped}
    return render(request, 'accounts/user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    """this function handles account settings update"""

    customer = request.user.customer #get the current logged in customer
    form = CustomerForm(instance=customer) #tie this form to the user

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer) #request.files becauses files are also uploaded

        if form.is_valid(): 
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def products(request):
    """This function renders the product page"""

    #database queries
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'accounts/products.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, customer_id):
    """this function handles the customer pages"""

    #database queries
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    order_count = orders.count()

    #the block below handles the actual filtration of product data
    myFilter = OrderFilter(request.GET, queryset=orders) #request.get because the filter is actually getting and filtering data from the database
    orders = myFilter.qs #myfilter.queryset

    context = {'customer':customer,'orders': orders, 'order_count':order_count, 'myFilter': myFilter,}
    return render(request, 'accounts/customer.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, customer_id): #
    """This function handles the creation of orders"""

    #the block below sets up the formset to be used for product orders 
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 ) #first instance of our formset with customer as parent model and order as child model
    customer = Customer.objects.get(id=customer_id) 
    
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer) #the query set set to non eliminates prepopulation of the forms from the database
    #form = OrderForm(initial={'customer': customer}) #the 'initial' keyword ties the order to the customer
    
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        #form = OrderForm(request.POST) 
        formset = OrderFormSet(request.POST, instance=customer)

        #the block below checks if submitted data is valid before saving, and redirecting to the homepage
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset,}
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def updateOrder(request, order_id):
    """This function handles the Update of orders"""
    
    # the block below pre-populates the order update form
    order = Order.objects.get(id=order_id) #get the order with the particular id
    form = OrderForm(instance=order)    #pass it to the form of the particular order(instance)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) #the instance keyword ensures the order is an update of the previous and not a new one

        #the block below checks if submitted data is valid before saving, and redirecting to homepage
        if form.is_valid():
            form.save()
            return redirect('/') #redirect to home

    context = {'form': form, 'order':order,}
    return render(request, 'accounts/update_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def deleteOrder(request, order_id):
    """This function handles the removal of orders from the database"""

    #database queries
    order = Order.objects.get(id=order_id) #query database for a particular order

    if request.method == 'POST':
        order.delete()  #delete order
        return redirect('/') #redirect to home
    
    context = {'order' : order}
    return render(request, 'accounts/delete.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createRandomOrder(request):
    """this function allows random orders to be created"""
    
    form =  OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form,}
    return render(request, 'accounts/update_form.html', context)



@unauthenticated_users
def userRegister(request):
    """This route handles user registration"""

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
            #checks if form submission is valid
        if form.is_valid():
            user = form.save()
            #the post_save signal is activated at this point
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username + '.')
            return redirect('login')

    context = {'form':form,}
    return render(request, 'accounts/register.html', context)



@unauthenticated_users
def userLogin(request):
    """This function handles user login"""

    if request.method == 'POST':
        #get both the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate the user
        user = authenticate(request, username=username, password=password)

        #if user is present, login user and redirect to home
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.info(request, 'username or password is incorrect!')
            return redirect('login')

    context = {}
    return render(request, 'accounts/login.html', context)



def userLogout(request):
    """this function handles the logout functionality"""

    logout(request)
    return redirect('login')

