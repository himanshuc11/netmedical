from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import medicine_type, Medicines


# Create your views here.
def index(request):

    if request.user.is_authenticated:
        if "cart" not in request.session:
            request.session["cart"] = []

    queryset = Medicines.objects.all()
    
    return render(request, 'netmedsapp/index.html', {
        "medicines": queryset
    })


def show_medicine_by_name(request, name):
    queryset = Medicines.objects.filter(name__icontains=name)
    return render(request, "netmedsapp/search.html", {
        "queryset": queryset
    })

def show_genres(request):
    queryset = medicine_type.objects.all()
    return render(request, "netmedsapp/genres.html", {
        "queryset": queryset
    })

def show_medicine_by_genre(request, genre):
    queryset = Medicines.objects.filter(genres__medicine_genre__iexact=genre)
    print(queryset)
    return render(request, "netmedsapp/medicines_by_genres.html", {
        "queryset": queryset
    })

   
def medicine(request, name):
    queryset = Medicines.objects.filter(name=name)
    return render(request, "netmedsapp/search.html", {
        "queryset": queryset
    })


@login_required
def update_cart(request):
    data = json.loads(request.body)
    medicine = data['medicine']
    action = data['action']

    print(medicine)
    print(action)

    if "cart" not in request.session:
        request.session["cart"] = []

    # Add medicine to cart only once and delete only when it exists
    all_orders = request.session["cart"]
    if action == "Add":
        if medicine not in all_orders:
            all_orders += [medicine]
    if action == "Remove":
        if medicine in all_orders:
            all_orders.remove(medicine)

    request.session["cart"] = all_orders
    return JsonResponse('Cart is updated', safe=False)

@login_required
def checkout(request):
    if "cart" not in request.session:
        return HttpResponse('Please add something to the cart before proceedimg to checkout')
    
    orders_names = request.session["cart"]
    medicine_orders = Medicines.objects.filter(name__in=orders_names)

    total_price = 0
    for medicine in medicine_orders:
        total_price += float(medicine.price)

    return render(request, "netmedsapp/checkout.html", {
        "orders": medicine_orders,
        "price": total_price
    })


def single_medicine(request, medicine_name):
    medicine = Medicines.objects.filter(name=medicine_name)[0]
    return render(request, "netmedsapp/single_medicine.html", {
        "medicine": medicine
    })

# Login logout and register
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "netmedsapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "netmedsapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "netmedsapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "netmedsapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "netmedsapp/register.html")

