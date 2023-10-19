import json
import pymongo

from django.views import View
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from rest_framework import viewsets, serializers

from .tasks import send_order_confirmation_email
from .signals import service_added_to_cart, handle_service_added_to_cart
from .forms import UserCreationForm, ServiceForm
from .models import User, Service, Order, Basket, BasketService, OrderService


def logger(message):
    with open('../host_metrics_app.log', 'a') as f:
        f.write(json.dumps(message) + '\n')


def delete_service_from_cart(request, service_id):
    try:
        user = request.user
        basket = get_object_or_404(Basket, user=user)
        basket_service = get_object_or_404(BasketService, basket=basket, service=service_id)

        basket_service.delete()

        basket.number_of_services = basket.services.aggregate(total_services=Sum('basketservice__quantity'))['total_services'] or 0
        basket.save()

        message = {
            'status': 200,
            'message': f"The service has been removed from the cart.",
        }
        logger(message)

    except:
        message = {
            'status': 400,
            'message': f"Failed to remove service from cart.",
        }
        logger(message)

    return redirect('cart_view_detail')


def register(request):
    return render(request, "registration/register.html")


def detail(request, record_id):
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client['autoservise']
        collection = database['autoservice_app_service']

        record = collection.find_one({"id": int(record_id)})

        return render(request, 'basis/detail.html', {'record': record})

    except:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client['autoservise']
        collection = database['autoservice_app_service']

        record = collection.find_one({"id": int(record_id)})

        message = {
            'status': 400,
            'message': f"Failed to load service details.",
            'service': record
        }
        logger(message)


def cart_view_detail(request):
    try:
        username = request.user.username
        basket, created = Basket.objects.get_or_create(user__username=username)

        return render(request, 'basis/basket.html', {'basket': basket})

    except:
        username = request.user.username
        message = {
            'status': 400,
            'message': f"Failed to load cart details.",
            'user': username
        }
        logger(message)


service_added_to_cart.connect(handle_service_added_to_cart)


def add_to_basket(request, record_name, username):
    try:
        quantity = request.POST.get('quantity', 1)
        try:
            service = Service.objects.get(name=record_name)
            user = User.objects.get(username=username)
        except:
            return redirect('list_of_services')

        basket, created = Basket.objects.get_or_create(user=user)

        basket_service, created = BasketService.objects.get_or_create(basket=basket, service=service)
        basket_service.quantity += int(quantity)
        basket_service.save()

        basket.number_of_services = basket.services.aggregate(total_services=Sum('basketservice__quantity'))['total_services'] or 0
        basket.save()

        service_added_to_cart.send(sender=request, request=request, service_name=record_name)

        message = {
            'status': 200,
            'message': f"Service added to cart.",
        }
        logger(message)

    except:
        service = Service.objects.get(name=record_name)
        message = {
            'status': 400,
            'message': f"Failed to load to cart",
        }
        logger(message)

    return redirect('list_of_services')


def create_order(request, sum_price):
    try:
        if request.method == 'POST':
            user = request.user
            basket = Basket.objects.get(user=user)

            order = Order.objects.create(customer_nickname=user.username, price=sum_price)

            for basket_service in basket.basketservice_set.all():
                order_service = OrderService.objects.create(order=order, service=basket_service.service, quantity=basket_service.quantity)

            send_order_confirmation_email.delay(user.email, sum_price)

            basket.services.clear()
            basket.number_of_services = 0
            basket.save()

            messages.success(request, 'Order has been created and email confirmation sent.')
            message = {
                'status': 200,
                'message': f"Order has been created and email confirmation sent.",
            }
            logger(message)

            return redirect('list_of_services')

    except:
        message = {
            'status': 400,
            'message': f"The order was not processed.",
        }
        logger(message)

    return redirect('list_of_services')


def list_of_services(request):
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client['autoservise']
        collection = database['autoservice_app_service']

        data_from_mongodb = collection.find()

        return render(request, 'basis/list_of_services.html', {'data': data_from_mongodb})

    except:
        message = {
            'status': 400,
            'message': f"Error loading service data.",
        }
        logger(message)


def create_a_service(request):
    try:
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = ServiceForm()

        message = {
            'status': 200,
            'message': f"Service created successfully."
        }
        logger(message)

        return render(request, 'basis/create_service.html', {'form': form})

    except:
        message = {
            'status': 400,
            'message': f"An error occurred while creating the service.",
        }
        logger(message)


def login(request):
    return render(request, "registration/login.html")


def home(request):
    return render(request, "basis/home.html")


def register_to_mongo(request):
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        registration = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        registration.save()

        message = {
            'status': 200,
            'message': f"Success register to mongo.",
            'user': username
        }
        logger(message)

    except:
        username = request.POST.get('username')
        message = {
            'status': 400,
            'message': f"Failed to register to mongo.",
            'user': username
        }
        logger(message)

    return render(request, "registration/register.html")


def check_user_exists(username):
    try:
        matching_users = User.objects.filter(username=username)
        user_exists = matching_users.exists()

        return user_exists

    except:
        message = {
            'status': 400,
            'message': f"User does not exist.",
            'user': username
        }
        logger(message)


def if_login(request):
    try:
        username = request.GET.get('username')
        user_exists = check_user_exists(username)

        message = {
            'status': 200,
            'message': f"user is authorized.",
            'user': username
        }
        logger(message)

        return render(request, 'registration/login.html', {'user_exists': user_exists})

    except:
        username = request.GET.get('username')
        message = {
            'status': 400,
            'message': f"Failed to load service details.",
            'user': username
        }
        logger(message)


class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        try:
            context = {
                "form": UserCreationForm()
            }
            return render(request, self.template_name, context)

        except:
            message = {
                'status': 400,
                'message': f"An error occurred during registration."
            }
            logger(message)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('first')
        else:
            return render(request, self.template_name, {
                'form': form
            })


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceView(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
