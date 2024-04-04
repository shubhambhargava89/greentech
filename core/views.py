from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *

from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
from razorpay import Client
from django.http import JsonResponse
import razorpay
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from reportlab.pdfgen import canvas

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


# Create your views here.


def admin_profile(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = request.user
    adm = AdminProfile.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['email']

        adm.user.first_name = f
        adm.user.last_name = l
        adm.contact_number = con
        adm.user.email = gen

        try:
            adm.save()
            adm.user.save()
            error = "no"

        except:
            error = "yes"

    d = {'adm': adm, 'error': error}
    return render(request, 'admin_profile.html', d)


def user_index(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    d = {'products': products}
    return render(request, 'user_index.html', d)


def index(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    d = {'products': products}
    return render(request, 'index.html', d)


def admin_index(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount = Enquiry.objects.all().count()
    scount = CustomerLogin.objects.all().count()
    pcount = Product.objects.all().count()
    ocount = OrderPlaced.objects.all().count()
    fcount = Feedback.objects.all().count()
    d = {'rcount': rcount, 'scount': scount, 'pcount': pcount, 'ocount': ocount, 'fcount':fcount}
    return render(request, 'admin_index.html', d)


def admin_view_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = CustomerLogin.objects.all()
    d = {'data': data}
    return render(request, 'admin_view_user.html', d)


def admin_delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('admin_view_user')


def admin_delete_product(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    pro = Product.objects.get(id=pid)
    pro.delete()
    return redirect('admin_view_product')


def change_status(request, oid):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        try:
            order = OrderPlaced.objects.get(id=oid)
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully.')
        except OrderPlaced.DoesNotExist:
            messages.error(request, 'Order not found.')

    # Redirect to the same page or any other page as per your requirement
    return redirect('admin_view_order')


def cancel_order(request,oid):
    if request.method == 'POST':
        try:
            order = OrderPlaced.objects.get(id=oid)
            order.status = 'Cancelled'
            order.save()
            messages.success(request, 'Order cancelled successfully')
        except OrderPlaced.DoesNotExist:
            messages.error(request, 'Cannot cancel delivered order')
    else:
        return redirect('orders')


def admin_edit_product(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    pro = Product.objects.get(id=pid)
    if request.method == "POST":
        f = request.POST['pname']
        ln = request.POST['price']
        c = request.POST['rating']
        g = request.POST['category']
        e = request.POST['detail']
        a = request.POST['quantity']
        i = request.FILES['image']

        pro.name = f
        pro.price = ln
        pro.rating = c
        pro.category = g
        pro.description = e
        pro.quantity = a
        pro.product_image = i

        try:
            pro.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error, 'pro': pro}
    return render(request, 'admin_edit_product.html', d)


def admin_view_order(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = OrderPlaced.objects.all()
    d = {'data': data}
    return render(request, 'admin_view_order.html', d)


def admin_view_enquiry(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Enquiry.objects.all()
    d = {'data': data}
    return render(request, 'admin_view_enquiry.html', d)


def view_feedback(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Feedback.objects.all()
    d = {'data': data}
    return render(request, 'view_feedback.html', d)


def admin_view_product(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Product.objects.all()
    d = {'data': data}
    return render(request, 'admin_product_dashboard.html', d)


def admin_add_product(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        f = request.POST['pname']
        ln = request.POST['price']
        c = request.POST['rating']
        g = request.POST['category']
        e = request.POST['detail']
        a = request.POST['quantity']
        i = request.FILES['image']
        try:
            Product.objects.create(name=f, price=ln, rating=c, category=g, description=e, quantity=a,
                                   product_image=i)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_add_product.html', d)


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('pass')
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                error = "no"  # Successful login
            else:
                error = "Invalid username or password"  # Non-staff user
        else:
            error = "Account Not Present"  # Authentication failed
    d = {'error': error}
    return render(request, 'admin_login.html', d)


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pass']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = CustomerLogin.objects.get(user=user)
                if user1.type == "customer":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_login.html', d)


def add_feedback(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        ln = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']
        e = request.POST['email']
        a = request.POST['about']
        try:
            Feedback.objects.create(firstname=f, lastname=ln, mobile=c, gender=g, mail=e, about=a,
                                   creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_feedback.html',d)


def user_profile(request):
    user = request.user
    user2 = CustomerLogin.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        e = request.POST['email']
        gen = request.POST['gender']

        user2.user.first_name = f
        user2.user.last_name = l
        user2.contact_number = con
        user2.user.email = e
        user2.gender = gen
        try:
            user2.save()
            user2.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'user2': user2, 'error': error}
    return render(request, 'user_profile.html', d)


def contact(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        ln = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']
        e = request.POST['email']
        a = request.POST['about']
        try:
            Enquiry.objects.create(firstname=f, lastname=ln, mobile=c, gender=g, mail=e, about=a,
                                   creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'contact.html', d)


def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['name']
        e = request.POST['mail']
        p = request.POST['pass']
        try:
            user = User.objects.create_user(first_name=f, username=f, password=p, email=e)
            CustomerLogin.objects.create(user=user, email=e, type="customer")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_signup.html', d)


def new_address(request):
    user = request.user
    error = ""
    if request.method == 'POST':
        f = request.POST['fullname']
        ad1 = request.POST['address1']
        ad2 = request.POST['address2']
        c = request.POST['city']
        s = request.POST['state']
        con = request.POST['contact']
        pin = request.POST['pincode']
        try:
            UserAddres.objects.create(user=user, name=f, address1=ad1, address2=ad2, city=c, state=s, contact=con,
                                      pincode=pin)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_new_address.html', d)


def existing_address(request):
    add = UserAddres.objects.filter(user=request.user)
    return render(request, 'user_address.html', {'add': add, 'active': 'btn-primary'})


def Logout(request):
    logout(request)
    return redirect('index')


def checkout(request):
    totalitem = 0
    user = request.user
    add = UserAddres.objects.filter(user=user)
    cart_items = CartItem.objects.filter(user=user)
    amount = Decimal(0.0)
    totalamount = Decimal(0.0)
    shipping_amount = Decimal(70.0)
    cart_product = [p for p in CartItem.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount = Decimal(p.quantity) * p.product.price
        amount += tempamount
    totalamount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(CartItem.objects.filter(user=request.user))
    return render(request, 'checkout.html',{'add': add , 'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})


def payment_done(request):
    if request.method == 'GET':
        payment_id = request.GET.get('payment_id')
        if payment_id:
            # Initialize Razorpay client with your API key and secret
            client = razorpay.Client(auth=("rzp_test_Kw423PWX9hLuGl", "R8GatWDvqy75pccVzbHR4LWD"))

            try:
                # Fetch payment details using the payment ID
                payment = client.payment.fetch(payment_id)
                user = request.user

                customer = CustomerLogin.objects.get(user=user)
                cart = CartItem.objects.filter(user=user)
                for c in cart:
                    OrderPlaced(user=user, customer=customer, product=c.product,
                                quantity=c.quantity, payment_id=payment_id, ordered_date=date.today()).save()
                    c.delete()
                return redirect("orders")
            except Exception as e:
                # Handle exceptions if any
                return HttpResponse("Error processing payment: " + str(e))
        else:
            # Handle if payment ID is not provided
            return HttpResponse("Payment ID is missing.")
    elif request.method == 'POST':
        # Handle Cash on Delivery payment
        user = request.user
        customer = CustomerLogin.objects.get(user=user)
        cart = CartItem.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product,
                        quantity=c.quantity, payment_id="Cash on Delivery", ordered_date=date.today()).save()
            c.delete()
        return redirect("orders")
    else:
        # Handle if request method is not GET or POST
        return HttpResponse("Invalid request method.")


def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(CartItem.objects.filter(user=request.user))
    return render(request, 'order_placed.html', {'order_placed':op,'totalitem':totalitem})


class ProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        return render(request, 'productdetail.html', {'product': product, 'totalitem': totalitem})


class AdminProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        p = Product.objects.get(pk=pk)
        return render(request, 'admin_eye.html', {'product': p, 'totalitem': totalitem})


class UserProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        return render(request, 'user_product_detail.html', {'product': product, 'totalitem': totalitem})


def swh(request, data=None):
    totalitem = 0
    if data == None:
        swh = Product.objects.filter(category='swh')
    return render(request, 'solar_water_heater.html', {'swh': swh, 'totalitem': totalitem})


def on(request, data=None):
    totalitem = 0
    if data == None:
        on = Product.objects.filter(category='on')
    return render(request, 'solar_on_grid.html', {'on': on, 'totalitem': totalitem})


def of(request, data=None):
    totalitem = 0
    if data == None:
        of = Product.objects.filter(category='of')
    return render(request, 'solar_off_grid.html', {'of': of, 'totalitem': totalitem})


def ss(request, data=None):
    totalitem = 0
    if data == None:
        ss = Product.objects.filter(category='ss')
    return render(request, 'solar_streetlight.html', {'ss': ss, 'totalitem': totalitem})


def sp(request, data=None):
    totalitem = 0
    if data == None:
        sp = Product.objects.filter(category='sp')
    return render(request, 'solar_pump.html', {'sp': sp, 'totalitem': totalitem})


def baseswh(request, data=None):
    totalitem = 0
    if data == None:
        swh = Product.objects.filter(category='swh')
    return render(request, 'base_solar_water_heater.html', {'swh': swh, 'totalitem': totalitem})


def baseon(request, data=None):
    totalitem = 0
    if data == None:
        on = Product.objects.filter(category='on')
    return render(request, 'base_solar_on_grid.html', {'on': on, 'totalitem': totalitem})


def baseof(request, data=None):
    totalitem = 0
    if data == None:
        of = Product.objects.filter(category='of')
    return render(request, 'base_solar_off_grid.html', {'of': of, 'totalitem': totalitem})


def basess(request, data=None):
    totalitem = 0
    if data == None:
        ss = Product.objects.filter(category='ss')
    return render(request, 'base_solar_streetlight.html', {'ss': ss, 'totalitem': totalitem})


def basesp(request, data=None):
    totalitem = 0
    if data == None:
        sp = Product.objects.filter(category='sp')
    return render(request, 'base_solar_pump.html', {'sp': sp, 'totalitem': totalitem})


def userswh(request, data=None):
    totalitem = 0
    if data == None:
        swh = Product.objects.filter(category='swh')
    return render(request, 'user_solar_water_heater.html', {'swh': swh, 'totalitem': totalitem})


def useron(request, data=None):
    totalitem = 0
    if data == None:
        on = Product.objects.filter(category='on')
    return render(request, 'user_solar_on_grid.html', {'on': on, 'totalitem': totalitem})


def userof(request, data=None):
    totalitem = 0
    if data == None:
        of = Product.objects.filter(category='of')
    return render(request, 'user_solar_off_grid.html', {'of': of, 'totalitem': totalitem})


def userss(request, data=None):
    totalitem = 0
    if data == None:
        ss = Product.objects.filter(category='ss')
    return render(request, 'user_solar_streetlight.html', {'ss': ss, 'totalitem': totalitem})


def usersp(request, data=None):
    totalitem = 0
    if data == None:
        sp = Product.objects.filter(category='sp')
    return render(request, 'user_solar_pump.html', {'sp': sp, 'totalitem': totalitem})


def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=user)
    if not created:
        # Convert quantity and stock to integers for comparison
        quantity = int(cart_item.quantity)
        stock = int(product.quantity)

        if quantity < stock:  # Check if quantity can be increased
            cart_item.quantity += 1
            cart_item.save()
    elif int(product.quantity) > 0:  # Check if there's available stock
        cart_item.quantity = 1
        cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def plus_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


def minus_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    price = sum(item.product.price * item.quantity for item in cart_items)
    shipping = int(70.0)
    total_price = price + shipping
    return render(request, 'cart.html', {'cart_items': cart_items, 'price': price, 'total_price': total_price})


def download_invoice(request, order_id):
    # Fetch order information from the database
    order = OrderPlaced.objects.get(id=order_id)
    total_amount = order.product.price * order.quantity

    # Generate invoice content (in this example, PDF format)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{slugify(order.id)}.pdf"'

    # Create PDF document
    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Invoice for Order #{order.id}')
    p.drawString(100, 780, f'Customer Name: {order.customer.user.username}')
    p.drawString(100, 760, f'Product: {order.product.name}')
    p.drawString(100, 740, f'Quantity: {order.quantity}')
    p.drawString(100, 720, f'Price per unit: {order.product.price}')  # Assuming price is stored in the Product model
    p.drawString(100, 700, f'Total Amount: {total_amount}')
    p.drawString(100, 680, f'Payment ID: {order.payment_id}')
    p.drawString(100, 660, f'Ordered Date: {order.ordered_date}')
    # Add more information as needed

    # Close PDF document
    p.showPage()
    p.save()

    return response

# def generate_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="Bill_Report.pdf"'
#
#     # Fetch all products from the database
#     products = Product.objects.all()
#
#     # Create a PDF document
#     doc = SimpleDocTemplate(response, pagesize=letter)
#     elements = []
#
#     styles = getSampleStyleSheet()
#     heading_style = styles['Heading1']
#     heading = Paragraph("Product Report", heading_style)
#     elements.append(heading)
#
#     # Define table data
#     data = [['Name', 'Price', 'Rating', 'Description', 'Category', 'Quantity']]
#
#     for product in products:
#         data.append([
#             product.name,
#             str(product.price),
#             str(product.rating),
#             product.description,
#             product.category,
#             str(product.quantity) if product.quantity else ''
#         ])
#
#     # Create a table and style
#     table = Table(data)
#     style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                         ('GRID', (0, 0), (-1, -1), 1, colors.black)])
#
#     table.setStyle(style)
#
#     # Add table to elements
#     elements.append(table)
#
#     # Build the PDF
#     doc.build(elements)
#     return response
