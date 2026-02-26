from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from AdminApp.models import *
from WebApp.models import *
from django.contrib import messages


# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")

def contact_details(request):
    contact = ContactDb.objects.all()
    return render(request, "contact_details.html",
                  {"contact" : contact})

def add_category(request):
    return render(request, "add_category.html")


def view_categories(request):
    category = CategoryDb.objects.all()
    return render(request, "view_categories.html",
                  {'data': category})


def save_category(request):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        cat_desc = request.POST.get("description")
        cat_img = request.FILES["cimg"]

        obj = CategoryDb(CategoryName=cat_name, Description=cat_desc, CategoryImage=cat_img)
        obj.save()
        messages.success(request, "Category Added !")
        return redirect(add_category)


def edit_category(request, cat_id):
    category = CategoryDb.objects.get(id=cat_id)
    return render(request, "edit_category.html",
                  {'cat': category})


def update_category(request, catg_id):
    if request.method == "POST":
        cat_name = request.POST.get("cname")
        cat_desc = request.POST.get("description")
        try:
            cat_img = request.FILES['cimg']
            fs = FileSystemStorage()
            file = fs.save(cat_img.name, cat_img)
        except MultiValueDictKeyError:
            file = CategoryDb.objects.get(id=catg_id).CategoryImage
        CategoryDb.objects.filter(id=catg_id).update(CategoryName=cat_name, Description=cat_desc,
                                                     CategoryImage=file)
        messages.success(request, "Category Updated !")
        return redirect(view_categories)


def delete_category(request, c_id):
    cat = CategoryDb.objects.filter(id=c_id)
    cat.delete()
    messages.success(request, "Category Deleted !")
    return redirect(view_categories)


# __________________________________________________________________________________________

def add_product(request):
    categories = CategoryDb.objects.all()
    return render(request, "add_product.html",
                  {'cat': categories})


def save_products(request):
    if request.method=="POST":
        p_name = request.POST.get('pname')
        c_name = request.POST.get('cname')
        description = request.POST.get('desc')
        price = request.POST.get('price')
        p_img = request.FILES['p_img']

        prod = ProductDb(ProductName=p_name, Category_Name=c_name, P_Description=description,
                        Price=price, ProductImage=p_img)
        prod.save()
        messages.success(request, "Product Added !")

        return redirect(add_product)



def view_products(request):
    products = ProductDb.objects.all()
    return render(request, "view_products.html",
                  {"prod" : products})

def edit_products(request, prod_id):
    product = ProductDb.objects.get(id=prod_id)
    category = CategoryDb.objects.all()
    return render(request, "edit_products.html",
                  {"pro" : product, "cat" : category})

def update_products(request, pro_id):
    if request.method=="POST":
        prod_name = request.POST.get("pname")
        catg_name = request.POST.get("cname")
        price = request.POST.get("price")
        prod_desc = request.POST.get("desc")
        try:
            prod_img = request.FILES["p_img"]
            fs = FileSystemStorage()
            file = fs.save(prod_img.name, prod_img)
        except MultiValueDictKeyError:
            file = ProductDb.objects.get(id=pro_id).ProductImage
        ProductDb.objects.filter(id=pro_id).update(ProductName=prod_name, Category_Name=catg_name,
                                                   P_Description=prod_desc,Price=price, ProductImage=file)
        messages.success(request, "Product Updated !")

        return redirect(view_products)

def delete_products(request, pro_id):
    product = ProductDb.objects.filter(id=pro_id)
    product.delete()
    messages.success(request, "Product Deleted !")
    return redirect(view_products)

#_________________________________________________________________________________________________________





def admin_loginpage(request):
    return render(request, "admin_login.html")


def admin_login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        if User.objects.filter(username__contains=uname).exists():
            user = authenticate(username=uname, password=passw)

            if user is not None:
                login(request, user)
                request.session['username'] = uname
                request.session['password'] = passw
                return redirect(dashboard)
            else:
                return redirect(admin_loginpage)
        else:
            messages.error(request, "Invalid username or password")
            return redirect(admin_loginpage)


def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_loginpage)
