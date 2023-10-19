from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from django.contrib import messages

from .models import User, Basket


@receiver(post_save, sender=User)
def create_user_basket(sender, instance, created, **kwargs):
    if created:
        Basket.objects.create(number_of_services=0)


service_added_to_cart = Signal('service_name')


@receiver(service_added_to_cart)
def handle_service_added_to_cart(sender, request, service_name, **kwargs):
    if request is not None and service_name is not None:
        messages.success(request, f"'{service_name}' has been added to the basket.")