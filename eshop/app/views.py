from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


# Create your views here.


def shp_login(req):
    if 'eshop' in req.session:
        return redirect(shp_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['eshop']=uname   #create session
                return redirect(shp_home)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shp_login)
    
    else:
        return render(req,'login.html')

def shp_home(req):
    if 'eshop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'data':data})
    else:
        return redirect(shp_login)

def shp_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(shp_login)

def add_prod(req):
    if 'eshop' in req.session:
        if req.method == 'POST':
            prd_id = req.POST['prd_id']
            prd_name = req.POST['prd_name']
            prd_price = req.POST['prd_price']
            ofr_price = req.POST['ofr_price']
            img = req.FILES['img']
            prd_dis = req.POST['prd_dis']
            prd_ram = req.POST['ram']  # Added RAM field
            prd_storage = req.POST['storage']  # Added Storage field

            # Create the new product including RAM and Storage
            data = Product.objects.create(
                pro_id=prd_id,
                name=prd_name,
                price=prd_price,
                ofr_price=ofr_price,
                img=img,
                dis=prd_dis,
                ram=prd_ram,  # Set the RAM value
                storage=prd_storage  # Set the Storage value
            )
            data.save()
            return redirect(add_prod)
        else:
            return render(req, 'shop/add_prod.html')
    else:
        return redirect(shp_login)

    
def edit_prod(req, pid):
    if 'eshop' in req.session:
        if req.method == 'POST':
            prd_id = req.POST['prd_id']
            prd_name = req.POST['prd_name']
            prd_price = req.POST['prd_price']
            ofr_price = req.POST['ofr_price']
            prd_dis = req.POST['prd_dis']
            prd_ram = req.POST['ram']  # Added RAM field
            prd_storage = req.POST['storage']  # Added Storage field
            img = req.FILES.get('img')
            
            if img:
                # Update the product with new RAM, Storage, and Image
                Product.objects.filter(pk=pid).update(
                    pro_id=prd_id,
                    name=prd_name,
                    price=prd_price,
                    ofr_price=ofr_price,
                    dis=prd_dis,
                    ram=prd_ram,  # Update the RAM value
                    storage=prd_storage  # Update the Storage value
                )
                data = Product.objects.get(pk=pid)
                data.img = img
                data.save()
            else:
                # Update the product without changing the image
                Product.objects.filter(pk=pid).update(
                    pro_id=prd_id,
                    name=prd_name,
                    price=prd_price,
                    ofr_price=ofr_price,
                    dis=prd_dis,
                    ram=prd_ram,  # Update the RAM value
                    storage=prd_storage  # Update the Storage value
                )
            return redirect(shp_home)
        else:
            data = Product.objects.get(pk=pid)
            return render(req, 'shop/edit.html', {'product': data})
    else:
        return redirect(shp_login)

def delete_prod(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(shp_home)
def bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'buy':buy})
#______________________________________________________________________USER___________________________________________________________________________________________________________________________________________________________________
def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(shp_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
    else:
        return render(req,'user/register.html')

def user_home(req):
    if 'user' in req.session:
        ram_filter = req.GET.get('ram')
        storage_filter = req.GET.get('storage')

        # Fetch products based on filters
        products = Product.objects.all()
        
        if ram_filter:
            products = products.filter(ram=ram_filter)
        if storage_filter:
            products = products.filter(storage=storage_filter)

        return render(req, 'user/home.html', {'data': products})
    else:
        return redirect(shp_login)

    
def view_pro(req, pid):
    data = Product.objects.get(pk=pid)
    return render(req, 'user/view_pro.html', {'data': data})


def add_to_cart(req, pid):
    prod = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])
    
    # Get the selected RAM and Storage from the form
    ram = req.POST.get('ram', prod.ram)  # Default to the product's RAM if not specified
    storage = req.POST.get('storage', prod.storage)  # Default to the product's Storage if not specified
    
    # Create the cart entry
    cart_item = Cart.objects.create(user=user, product=prod, ram=ram, storage=storage)
    cart_item.save()
    return redirect(view_cart)


# views.py

def view_cart(req):
    user = User.objects.get(username=req.session['user'])
    cart_dtls = Cart.objects.filter(user=user)
    return render(req, 'user/cart.html', {'cart_dtls': cart_dtls})


def delete_cart(req,id):
    cart=Cart.objects.get(pk=id)
    cart.delete()
    return redirect(view_cart)

def user_buy(req,cid):
    user=User.objects.get(username=req.session['user'])
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    price=cart.product.ofr_price
    buy=Buy.objects.create(user=user,product=product,price=price)
    buy.save()
    return redirect(order_create)
def user_buy1(req,pid):
     user=User.objects.get(username=req.session['user'])
     product=Product.objects.get(pk=pid)
     price=product.ofr_price
     buy=Buy.objects.create(user=user,product=product,price=price)
     buy.save()
     return redirect(order_create)
def user_booking(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'buy':buy})



def remove_booking(request, booking_id):
    # Get the booking object by its ID or return a 404 if it doesn't exist
    booking = get_object_or_404(Buy, id=booking_id)
    
    # Delete the booking
    booking.delete()
    
    # Redirect to the 'user_booking' page using the correct URL name
    return redirect('user_booking')  # Ensure 'user_booking' is the correct name in your URLs


# views.pydef add_to_cart(req, pid):
    prod = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])
    data = Cart.objects.create(user=user, product=prod)  # Don't pass ram and storage here
    data.save()
    return redirect('view_cart')

# views.py

def add_to_cart(req, pid):
    prod = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])
    data = Cart.objects.create(user=user, product=prod)
    data.save()
    return redirect('view_cart')  # Ensure 'view_cart' is the correct URL pattern name


from django.shortcuts import render, redirect
from .form import OrderForm
from .models import Order

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success')  # Redirect to success page
    else:
        form = OrderForm()
    
    return render(request, 'user/order.html', {'form': form})

def order_success(request):
    return render(request, 'user/order_success.html')
