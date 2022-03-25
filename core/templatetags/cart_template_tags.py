from django import template
from core.models import Basket

register = template.Library()


@register.filter
def cart_product_count(request):
    print(request)
    if request.user.is_authenticated:
        qs = Basket.objects.filter(user=request.user, is_ordered=False)
        if qs.exists():
            return qs[0].products.count()
        return 0
    else:
        if request.session.get('has_cart', None) == '1' and request.session.get('cart_id', None) is not None:
            order_query = Basket.objects.filter(
                pk=request.session['cart_id'], is_ordered=False)
            if order_query.exists():
                return order_query[0].products.count()
        else:
            return 0


@register.filter
def cart_total_summary(request):
    if request.user.is_authenticated:
        order_qs = Basket.objects.filter(user=request.user, is_ordered=False).prefetch_related(
            'products').prefetch_related('products__extraoptionordered_set')
    elif request.session.get('has_cart', None) is '1' and request.session.get('cart_id', None) is not None:
        order_qs = Basket.objects.filter(
            pk=request.session['cart_id'], is_ordered=False).prefetch_related('products').prefetch_related('products__extraoptionordered_set')
    else:
        return 0
    if order_qs.exists() and order_qs is not None:
        order = order_qs[0]
        order_products = order.products.filter()
        total_summary = 0
        for order_product in order_products:
            extra_options_cost = 0
            if order_product.product.discount_price is not None and order_product.product.discount_price > 0:
                order_product_discount_price = order_product.product.discount_price
                order_product_total_summary = order_product_discount_price * order_product.quantity
            else:
                order_product_price = order_product.product.price
                order_product_total_summary = order_product_price * order_product.quantity
            for extra_option in order_product.extraoptionordered_set.all():
                extra_options_cost += extra_option.cost * extra_option.count
            order_product_total_summary += extra_options_cost
            total_summary += order_product_total_summary
    else:
        return 0

    return total_summary
