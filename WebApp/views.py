from django.shortcuts import render, redirect
from unicodedata import category

from AdminApp.models import *
from AdminApp.views import delete_products
from WebApp.models import *
from django.contrib import messages

# Create your views here.

def home_page(request):
    categories = CategoryDb.objects.all()
    latest_products = ProductDb.objects.order_by('-id')[:8]
    uname=request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()

    return render(request, "home.html",
                  {"categories" : categories,
                            "latest_products" : latest_products,
                            "cart" : cart_count
                   })

def all_products(request):
    categories = CategoryDb.objects.all()
    products = ProductDb.objects.all()
    latest_products = ProductDb.objects.order_by('-id')[:3]
    latest_products1 = ProductDb.objects.order_by('-id')[4:7]
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    return render(request, "all_products.html",
                  {"categories" : categories,
                            "products" : products,
                            "latest_products" : latest_products,
                            "latest_products1" : latest_products1,
                            "cart" : cart_count})

def filtered_products(request, cat_name):
    products_filtered = ProductDb.objects.filter(Category_Name=cat_name)
    categories = CategoryDb.objects.all()
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    return render(request, "filtered_products.html",
                  {"products" : products_filtered,
                            "categories" : categories,
                            "cart" : cart_count})

def single_item(request, product_id):
    single_item = ProductDb.objects.get(id=product_id)
    return render(request, "single_item.html",
                  {"single" : single_item})


#_______________________________________________________________________________________________________

def about(request):
    categories = CategoryDb.objects.all()
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    return render(request, "about.html",
                  {"cart": cart_count,
                   "categories": categories})
def services(request):
    categories = CategoryDb.objects.all()
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    return render(request, "services.html",
                  {"cart" : cart_count,
                            "categories" : categories})

def contact(request):
    categories = CategoryDb.objects.all()
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    return render(request, "contact.html",
                  {"categories" : categories,
                            "cart" : cart_count})

def save_message(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        obj = ContactDb(Name=name, Email=email, Message=message)
        obj.save()

        return redirect(contact)

# ______________________________User Registration____________________________________

def signin(request):
    return render(request, "signin.html")

def signup(request):
    return render(request, "signup.html")

def save_user(request):
    if request.method=="POST":
        u_name = request.POST.get('uname')
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        c_pswd = request.POST.get('cpswd')

        obj = SignupDb(Username=u_name, Email=email, Password=pswd, C_Password=c_pswd)
        if SignupDb.objects.filter(Username=u_name).exists():
            print("Username Already Exists")
            return redirect(signup)
        elif SignupDb.objects.filter(Email=email).exists():
            print("Email Already Exists")
            return redirect(signup)
        else:
            obj.save()
            return redirect(signin)

def user_login(request):
    if request.method=="POST":
        uname = request.POST.get('username')
        pswd = request.POST.get('password')

        if SignupDb.objects.filter(Username=uname, Password=pswd).exists():
            request.session['Username'] = uname
            request.session['Password'] = pswd
            return redirect(home_page)
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(signin)

    else:
        return redirect(signin)

def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(home_page)

#___________________________________________________________________________________________________________

def cart(request):
    data = CartDb.objects.filter(Username=request.session['Username'])
    categories = CategoryDb.objects.all()
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    sub_total = 0
    delivery = 0
    grand_total = 0

    for i in data:
        sub_total += i.Total_Price
        if sub_total > 500:
            delivery = 0
        elif sub_total > 400:
            delivery = 50
        else:
            delivery = 100
        grand_total = sub_total + delivery

    return render(request, "cart.html",
                  {"data" : data, "sub_total" : sub_total,
                           "delivery" : delivery, "grand_total" : grand_total,
                            "cart" : cart_count,
                            "categories" : categories})

def add_to_cart(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        product = request.POST.get('pname')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        total = request.POST.get('total')
        pro = ProductDb.objects.filter(ProductName=product).first()
        img = pro.ProductImage if pro else None
        obj = CartDb(Username=uname, Product_Name=product, Price=price,
                     Quantity=quantity, Total_Price=total, Product_Image=img)
        obj.save()

    return redirect(cart)

def checkout(request):
    if request.method=="POST":
        first = request.POST.get('first')
        last = request.POST.get('last ')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        total = request.POST.get('total')

        obj = OrderDb(FirstName=first, LastName=last, State=state, City=city, Address=address,
                      Postcode=postcode, Email=email, Mobile=mobile, GrandTotal=total)
        obj.save()

        return redirect(payment_page)

    data = CartDb.objects.filter(Username=request.session['Username'])
    uname = request.session.get('Username')
    cart_count = 0
    if uname:
        cart_count = CartDb.objects.filter(Username=uname).count()
    sub_total = 0
    delivery = 0
    grand_total = 0

    for i in data:
        sub_total += i.Total_Price
        if sub_total > 500:
            delivery = 0
        elif sub_total > 400:
            delivery = 50
        else:
            delivery = 100
        grand_total = sub_total + delivery
    return render(request, "checkout.html",
                  {"data" : data, "sub_total" : sub_total,
                            "delivery" : delivery, "grand_total" : grand_total,
                            "cart_count" : cart_count})

def delete_items(request, item_id):
    items = CartDb.objects.filter(id=item_id)
    items.delete()
    return redirect(cart)

def payment_page(request):
    return render(request, "payment.html")

