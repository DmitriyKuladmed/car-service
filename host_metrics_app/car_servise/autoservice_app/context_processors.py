from .models import Basket


def basket_item_count(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).first()
        if basket:
            return {'basket_item_count': basket.number_of_services}
    return {'basket_item_count': 0}