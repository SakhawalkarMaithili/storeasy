from email import message
from django.shortcuts import render, redirect   # redirect is new

from django.http import HttpResponse

from django.forms import inlineformset_factory  # new

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

# Create your views here.

def registerPage (request):
    # if a user is already logged in, he should not be able to access the register page
    if request.user.is_authenticated:
        return redirect ('home')

    else:
        # form = UserCreationForm()
        form = CreateUserForm()

        if request.method == 'POST':
            # form = UserCreationForm (request.POST)
            form = CreateUserForm (request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account created for " + user)
                return redirect('login')

        context = {'form':form}
        return render (request, 'accounts/register.html', context)

def loginPage (request):
    # if a user is already logged in, he should not be able to access the register page
    if request.user.is_authenticated:
        return redirect ('home')

    else:        
        if request.method == 'POST':
            username = request.POST.get ('username')       # the data will be taken from the html form with field whose name = 'username'
            password = request.POST.get ('password')

            user = authenticate (request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info (request, 'Username or Password Incorrect')

        context = {}
        return render (request, 'accounts/login.html')

def logoutUser (request):
    logout(request)
    # print (request)
    return redirect ('login')

@login_required (login_url = 'login')
def home (request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter (status='Delivered').count()
    pending = orders.filter (status='Pending').count()

    
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}          # instead of writing the whole dictionary as a parameter, we create a separate variable for it and add it as a parameter. Just for our convenience

    return render (request, 'accounts/dashboard.html', context)
    
'''_______________________________________________________________________________________________________________________'''

# def products (request):
#     return HttpResponse ('products')

# def products (request):
#     return render (request, 'accounts/products.html')

@login_required (login_url = 'login')
def products (request):
    products = Product.objects.all()
    return render (request, 'accounts/products.html', {'products':products})                # last parameter is a dictionary. We can use anything for key instead of 'products' (e.g. {'list' : products})

'''_______________________________________________________________________________________________________________________'''

# def customer (request):
#     return HttpResponse ('customer')

@login_required (login_url = 'login')
def customer (request, pk):         # pk - primary key -> so that we can use the same template to display different customers ___NOTE__ The variable, i.e. pk in this case should be named the same as in the <str:pk> field in urls.py. e.g. If we have written <str:primkey>, we have to write def customer (request, primkey)
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()

    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}

    return render (request, 'accounts/customer.html', context)

'''________________________________________________________________________________________________________________________'''

@login_required (login_url = 'login')
def createOrder (request, pk):
    # OrderFormSet = inlineformset_factory (Customer, Order, fields=('product', 'status'))    # Customer -> parent model; Order -> Child model; i.e. reference is from Order to Customer
    customer = Customer.objects.get(id=pk)

    # form = OrderForm() -> for an empty form
    form = OrderForm (initial={'customer':customer})
    # formset = OrderFormSet (instance=customer)

    # we are writing this here itself because we haven't redirected from the submit button. So, the post info will be sent to this page itself
    # and we specifically have to write this for POST request and not for GET is because GET is default
    if (request.method == 'POST'):
        # print ("Printing POST request : ", request.POST);
        form = OrderForm (request.POST)
        if form.is_valid ():
            form.save()                       # saves the form data to database
            return redirect ('/')             # will redirect to the homepage (dashboard). If we want to redirect to products, we would write return redirect ('/products/')

        # print ("Printing POST request : ", request.POST);
        # formset = OrderFormSet (request.POST, initial=customer)
        # if formset.is_valid():
        #     formset.save()
        #     return redirect ('/')


    # context = {'formset':formset}
    context = {'form':form}
    return render (request, 'accounts/order_form.html', context)


'''________________________________________________________________________________________________________________________'''

@login_required (login_url = 'login')
def updateOrder (request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if (request.method == 'POST'):
        form = OrderForm (request.POST, instance=order)
        if form.is_valid ():
            form.save()
            return redirect ('/')

    context = {'form' : form}
    return render (request, 'accounts/order_form.html', context)


'''________________________________________________________________________________________________________________________'''

@login_required (login_url = 'login')
def deleteOrder (request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect ('/')

    context = {'item':order}
    return render (request, 'accounts/delete.html', context)