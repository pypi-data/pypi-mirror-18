
from agiletix.cart import get_cart_for_request


class CartMiddleware(object):

    def process_request(self, request):
        cart = get_cart_for_request(request)
        return None


