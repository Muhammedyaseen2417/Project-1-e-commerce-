from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse


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
            prd_stock = req.POST['stock_quantity']  # Added Stock Quantity field

            # Create the new product including RAM, Storage, and Stock Quantity
            data = Product.objects.create(
                pro_id=prd_id,
                name=prd_name,
                price=prd_price,
                ofr_price=ofr_price,
                img=img,
                dis=prd_dis,
                ram=prd_ram,  # Set the RAM value
                storage=prd_storage,  # Set the Storage value
                quantity_in_stock=prd_stock  # Set the Stock Quantity
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
            prd_stock = req.POST['stock_quantity']  # Added Stock Quantity field
            img = req.FILES.get('img')
            
            if img:
                # Update the product with new RAM, Storage, Stock Quantity, and Image
                Product.objects.filter(pk=pid).update(
                    pro_id=prd_id,
                    name=prd_name,
                    price=prd_price,
                    ofr_price=ofr_price,
                    dis=prd_dis,
                    ram=prd_ram,  # Update the RAM value
                    storage=prd_storage,  # Update the Storage value
                    stock_quantity=prd_stock  # Update the Stock Quantity
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
                    storage=prd_storage,  # Update the Storage value
                    quantity_in_stock=prd_stock  # Update the Stock Quantity
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
def bookings(request):
    # Get all Buy objects with related product and user data
    buy = Buy.objects.select_related('product', 'user').all().order_by('-date')
    
    # Get all Order objects related to the Buy objects (assuming there's a way to link Buy to Order)
    orders = Order.objects.all()

    # Create combined data
    combined_data = zip(buy, orders)

    return render(request, 'shop/bookings.html', {'combined_data': combined_data})



from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string

# Mock function to simulate email sending for verification
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'















#______________________________________________________________________USER___________________________________________________________________________________________________________________________________________________________________

def register(req):
    if req.method == 'POST':
        fname = req.POST['fname']
        email = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['fname'] = fname
        req.session['password'] = password
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP sent to your email")
        return redirect('verify_otp')
    return render(req, 'user/register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        fname = req.session.get('fname')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=fname,email=email,password=password,username=email)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To Premium Home Cleaners', settings.EMAIL_HOST_USER, [email])
            return redirect('shp_login')
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect('verify_otp_reg')

    return render(req, 'user/verify_otp.html')

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

from django.shortcuts import redirect
from .models import User, Cart, Buy
from django.shortcuts import redirect
from .models import User, Cart, Buy

# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from .models import User, Cart, Buy, Product

# def user_buy(req, cid):
#     try:
#         user = User.objects.get(username=req.session['user'])
#         cart = Cart.objects.get(pk=cid)
#         product = cart.product
#         quantity_to_buy = cart.quantity  # Get the quantity from cart

#         # Check if enough stock is available
#         if product.quantity_in_stock >= quantity_to_buy:
#             price = product.ofr_price * quantity_to_buy  # Total price calculation

#             # Reduce stock by the purchased quantity
#             product.quantity_in_stock -= quantity_to_buy
#             product.save()

#             # Create an order entry for the user
#             buy = Buy.objects.create(user=user, product=product, price=price)
#             buy.save()

#             # Remove the item from the cart after purchase
#             cart.delete()

#             messages.success(req, f"You successfully bought {quantity_to_buy} units of {product.name}.")
#             return redirect(order_create)
#         else:
#             messages.error(req, f"Sorry, only {product.quantity_in_stock} units left in stock!")
#             return redirect('cart_page')  # Redirect back to cart if stock is insufficient

#     except Cart.DoesNotExist:
#         messages.error(req, "Cart item not found.")
#         return redirect('cart_page')

#     except User.DoesNotExist:
#         messages.error(req, "User not found. Please log in again.")
#         return redirect('login_page')

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Cart, Buy, Product

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
from django.http import HttpResponse



# views.py
from django.shortcuts import render

def homepage(request):
    return render(request, 'user/home1.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)  # Get product by ID
    return render(request, 'add_prod.html', {'product': product})

def update_stock(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        new_quantity = request.POST.get('quantity')
        
        if new_quantity is not None:
            product.quantity_in_stock = int(new_quantity)
            product.save()
            return redirect('product_detail', product_id=product.id)

    return HttpResponse("Invalid request", status=400)






from django.shortcuts import render, redirect
from .form import OrderForm
from .models import Order

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .form import OrderForm
from .models import Order  # Assuming you have an Order model

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the order form and create a new order in the database
            order = form.save()

            # Step 1: Create an order on Razorpay
            amount = 1000  # Calculate the total amount for the order, here it's 1000 paise (₹10)
            currency = 'INR'
            order_data = {
                'amount': amount * 100,  # Razorpay expects the amount in paise (100 paise = 1 INR)
                'currency': currency,
                'payment_capture': '1',  # 1 means automatic payment capture after successful payment
            }

            # Create the Razorpay order
            try:
                razorpay_order = razorpay_client.order.create(data=order_data)
                # Save the Razorpay order ID in your order model
                order.razorpay_order_id = razorpay_order['id']
                order.save()

                # Step 2: Pass the Razorpay order details to the template for frontend
                context = {
                    'order': order,
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_amount': amount * 100,  # Amount in paise
                    'razorpay_currency': currency,
                }

                # Render the payment page for the user to complete the payment
                return render(request, 'user/payment.html', context)

            except razorpay.errors.BadRequestError as e:
                # Handle error if something goes wrong with creating the order on Razorpay
                return render(request, 'user/error_page.html', {'error': str(e)})

    else:
        form = OrderForm()

    return render(request, 'user/order.html', {'form': form})




def order_success(request):
    return render(request, 'user/order_success.html')



from django.shortcuts import render, redirect
from .models import Order, Buy
import razorpay

def clear_all_orders2(request, order_id):
    try:
        # Fetch the order from the database using the order_id
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'error.html', {'message': 'Order not found'})

    # Fetch the associated 'buy' object (assuming it's related to the Order object)
    try:
        buy = Buy.objects.get(order=order)  # Assuming Buy model has a foreign key to Order
    except Buy.DoesNotExist:
        buy = None  # If there's no associated Buy object, set it to None

    # Debugging information to check if 'buy' and related data are present
    print("Buy object:", buy)
    if buy:
        print("Product details:", buy.product)
        print("Quantity:", buy.quantity)
        print("Total amount:", buy.total_amount)

    # Razorpay configuration
    razorpay_key_id = "your_razorpay_key_id"
    razorpay_amount = order.total_amount * 100  # Convert to paise (1 INR = 100 paise)
    razorpay_currency = "INR"
    
    # Create Razorpay order
    razorpay_client = razorpay.Client(auth=("rzp_test_fGXBbOpWsXJ5K7", "8r97uL39w4etyjunuKYO4tpE"))
    razorpay_order = razorpay_client.order.create(dict(
        amount=razorpay_amount,
        currency=razorpay_currency,
        payment_capture='1'
    ))

    context = {
        'buy': buy,  # Passing the buy object (which should include the product details)
        'razorpay_key_id': razorpay_key_id,
        'razorpay_amount': razorpay_amount,
        'razorpay_currency': razorpay_currency,
        'razorpay_order_id': razorpay_order['id'],
        'user': request.user
    }

    return render(request, 'user/payment.html', context)

















import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            # Extract the payment details sent by Razorpay
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            
            # Create a dictionary of payment verification details
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                
                # Handle success: Mark the order as paid in the database
                order = Order.objects.get(razorpay_order_id=order_id)
                order.payment_status = 'Paid'
                order.payment_id = payment_id
                order.save()

                # Redirect or render the success page
                return render(request, 'user/order_success.html', {'order': order})
            
            except razorpay.errors.SignatureVerificationError:
                return render(request, 'user/order_success.html')
        except Exception as e:
            return render(request, 'user/order_success.html')














