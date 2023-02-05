from django.shortcuts import render ,redirect,HttpResponse
from .models import Cart,Product,OrderPlaced,Customer 
from .forms import CustomerRegistrationForm ,LoginForm,CustomerProfile
from django.contrib import messages 
from django.contrib.auth.views import LoginView,LogoutView 
from django.contrib.auth import authenticate, logout
from django.views.generic.edit import CreateView 
from django.views import View 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q


def home(request):
    topwears=Product.objects.filter(category='TW')
    Bottomwears=Product.objects.filter(category='BW')
    mobiles=Product.objects.filter(category='M')
    
    return render(request, 'app/home.html',{'topwears':topwears,'Bottomwaers':Bottomwears,'mobiles':mobiles})
 
def product_detail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request, 'app/productdetail.html',{'product':product})


@login_required()
def add_to_cart(request):
    
     
    user=request.user
    form=Customer.objects.filter(user=request.user)
    if form:
        product_id=request.GET.get('prod_id')
        product=Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect('/showcart')
    else:
        return redirect("/address")



   
   
    
@login_required ()
def show_cart(request):
    user=request.user
    carts=Cart.objects.filter(user=user)
    amount=0.0
    base=0.0
    shiping_amount=70
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discount_price)
            amount+=tempamount
            if amount>=500:
                totalamount=amount + shiping_amount-shiping_amount
                base=0

            else:
                 totalamount=amount + shiping_amount
                 base=70
    else:
        return HttpResponse('<h1> your cart is empaty </h1>')
    return render(request, 'app/addtocart.html',{'amount':amount,'totalamount':totalamount,'carts':carts,'shiping_amount':shiping_amount,'base':base})
 

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity* p.product.discount_price)
			
			amount += tempamount
			
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			
			amount += tempamount
			
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


def delete_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount= 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
        return JsonResponse(data)
    else:
        return HttpResponse("")





def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    form=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'form':form})

def orders(request):
    
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'or':order_placed,})


def mobile(request,data=None):
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data=='redmi'or data=='Samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=10000)
      
  
    return render (request, 'app/mobile.html',{'mobiles':mobiles})

class Login(LoginView):
    template_name='app/login.html'
    authentication_form=LoginForm
    success_url='/profile/'
    
#customer signup form
class CustomerRegistration(CreateView):
    form_class=CustomerRegistrationForm
    template_name='app/customerregistration.html'
    success_url='/registration/'
    def form_valid(self, form):
        form.save()
        
        return super().form_valid(form)

def checkout(request):
    user=request.user
    
    carts=Cart.objects.filter(user=user)
    cust=Customer.objects.filter(user=user)

    return render(request, 'app/checkout.html',{'carts':carts,'customer':cust })
# orde

def order_done(request):
    custid = request.GET['custid'] #or request.GET.get('custid')
    print("Customer ID", custid)
    user = request.user
    cartid = Cart.objects.filter(user = user)
    customer = Customer.objects.get(id=custid)
    for cid in cartid:
        OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
        cid.delete()
    return redirect("orders")



# end

def profile(request):
 return render(request, 'app/profile.html')

class Profileviews(View):
    def get(self,request):
        totelatom=0
        if request.user.is_authenticated:
            totelatom=len(Cart.objects.filter(user=request.user))
            form=CustomerProfile()
        return render(request, 'app/profile.html',{'form':form,'totelatom':totelatom})
   
       

    def post(self,request):
        totelatom = 0
        if request.user.is_authenticated:
            totelatom=len(Cart.objects.filter(user=request.user))
        form=CustomerProfile(request.POST)

        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            zipcode=form.cleaned_data['zipcode']
            state=form.cleaned_data['state']

            reg=Customer(user=user,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
        return render(request, 'app/profile.html',{'form':form,'totelatom':totelatom})
