
from .cart import get_cart_for_request


def shopping_cart(request):
    return {
        'cart': get_cart_for_request(request)
    }

