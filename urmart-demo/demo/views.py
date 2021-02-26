from django.shortcuts import render
from common.models import Product, Order, Shop, ScheduleLog
# Create your views here.

def demo(request):
    """
    展示首頁
    """
    context = {}
    return render(request, 'demo/demo.html', context)
