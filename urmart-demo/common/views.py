from django.shortcuts import render
from common.models import Product, Order, Shop, ScheduleLog
# Create your views here.

def demo(request):
    """
    展示首頁
    """
    order_list = Order.objects.all() # get order list
    product_list = Product.objects.all() # get product list
    context = {
        "order_list": order_list,
        "product_list": product_list
    }
    return render(request, 'demo.html', context)
