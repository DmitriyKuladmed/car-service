from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('user', views.UserView)
router.register('service', views.ServiceView)
router.register('order', views.OrderView)


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("home/", views.home, name="home"),
    path("register/", views.Register.as_view(), name="register"),
    path("home/create_order/<int:sum_price>", views.create_order, name="create_order"),
    path("home/create_service/", views.create_a_service, name="create_service"),
    path("home/list_of_services/", views.list_of_services, name="list_of_services"),
    path("home/list_of_services/<int:record_id>", views.detail, name="detail"),
    path("home/cart_view_detail/", views.cart_view_detail, name="cart_view_detail"),
    path("home/add_to_basket/<str:record_name>/<str:username>", views.add_to_basket, name="add_to_basket"),
    path('delete_service/<int:service_id>/', views.delete_service_from_cart, name='delete_service'),
]

urlpatterns += router.urls

