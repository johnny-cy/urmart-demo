from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import Product, Order, Shop, ScheduleLog
from django.db.models import Count, F, Value
from django.db.models import Avg, Count, Min, Sum
import json
from django.core.exceptions import ValidationError
from web.consumers import ChatConsumer
from asgiref.sync import async_to_sync
import re
from datetime import datetime
import pandas as pd
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from asgiref.sync import sync_to_async
import asyncio

# Create your views here.

# validating decorator
def require_validation(function):
    def wrapper(request, *args, **kwargs):
        print("path:" , request.get_full_path_info())
        # print(dir(request))
        try:
            if "/urmart-api/AddOrder/" in request.get_full_path_info(): # for AddOrder
                post_data = json.loads(request.body)
                ValidateAddOrder(post_data)
            elif re.search( r"^/urmart-api/DelOrder/[0-9]+/$", request.get_full_path_info()) != None :
                print("in DelOrder Validator")
                
        except ValidationError as e:
            print(e)
            return HttpResponse(content=e, status=400)

        return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

def GetOrder(request, oid=None):
    """
    獲取訂單清單
    """
    if oid:
        data = Order.objects.filter(id=oid).values()
    else:
        data = Order.objects.values()
    return JsonResponse({"results": list(data)})

def GetProduct(request, pid=None):
    """
    獲取產品清單
    """
    if pid:
        data = Product.objects.filter(id=pid).values()
    else:
        data = Product.objects.values()
    print(data)
    return JsonResponse({"results": list(data)})

@require_validation
def AddOrder(request):
    """
    添加訂單
    """
    print("in add order")
    post_data = json.loads(request.body)
    p = Product.objects
    data = {
        "Product_id": p.get(id=post_data['pid']),
        "Qty": post_data['qty'],
        "Price": p.get(id=post_data['pid']).Price * int(post_data['qty']),
        "Shop_id": p.get(id=post_data['pid']).Shop_id.Shop_id,
        "Customer": post_data['cid']
    }
    try:
        o = Order.objects
        new_order_id = o.create(**data).id
        new_order_data = o.filter(id=new_order_id).values()
        p.filter(id=post_data['pid']).update(Stock_pcs=F('Stock_pcs') - 1 ) # or minus post_data['qty'] for future neeeds.
        
    except Exception as err:
        print(err)
        return JsonResponse({"results": {"error_message": f"unknown: {err}"}})
    
    return JsonResponse({"results": list(new_order_data)})

@require_validation
def DelOrder(request, oid):
    """
    刪除訂單 # should use transaction for multiple related operations in future.
    """
    try:
        o = Order.objects.get(id=oid)
        pid = o.Product_id.id
        qty = o.Qty 
        o.delete() 
    except Exception as err:
        return JsonResponse({"results": 0, "error_message": str(err)})
    try:
        Product.objects.filter(id=pid).update(Stock_pcs=F('Stock_pcs') + qty ) # return
    except Exception as e:
        print(e)
    return JsonResponse({"results": {"Pid": pid, "Qty": qty}})


async def GenReport(request):
    """
    產生文件並選擇發送郵件 (async)
    """
    
    @sync_to_async
    def do_thread():
            
        # TODO: Gen CSV, also attached and display, method GET
        try:
            data = Order.objects.values('Shop_id').annotate(orders_count=Count('id'), sold_pcs=Sum('Qty'), sales=Sum(F('Qty')*F('Price')))
            dt = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
            pd.DataFrame(data).to_csv(f'report_shop_{dt}.csv', index=False)
            subject = "訂單記錄統"
            body = "<h1>統計內容</H1><hr><H2>根據訂單記錄算出各個館別的1.總銷售金額 2.總銷售數量 3.總訂單數量<br><p>統計結果請見附件</p>"
            to = ['svmax0922@gmail.com', settings.EMAIL_HOST_USER]
            # to = [i.strip() for i in to ]
            mail = EmailMessage(
                subject = subject,
                body = body,
                from_email = settings.EMAIL_HOST_USER,
                to = to,
                headers = {"Message-ID": "foo"},
            )
            mail.attach_file(f'report_shop_{dt}.csv')
            mail.content_subtype = "html"
            mail.send()
            ScheduleLog.objects.create(**{
                "FuncName": "GenReport",
                "is_sent": 1,
                "To": str(to).replace("[", "").replace("]",""),
                "Comment": "-"
            })
            print("async sent. (should use a specific logger for async log in future)")
        except Exception as e:
            print(e)
            ScheduleLog.objects.create(**{
                "FuncName": "GenReport",
                "is_sent": 0,
                "To": str(to).replace("[", "").replace("]",""),
                "Comment": str(e)
            })
            print("faied sending shop report ..")
        print("shop report has been sent successfully!")

  
    def get_data():
        return 111
    d = get_data()
    print(d)
    task = asyncio.ensure_future(do_thread())
    return JsonResponse({"results": f'mail has been sent to address, , successfully.'})

def GetTop(request, num=3, order_by="sales_volume", order="asc"):
    """
    獲取產品排名
    """
    if order_by=='sales_volume': # strategy
        # 先將相同product_id的屬性qty相加
        top3 = Order.objects.values('Product_id').annotate(sales=Sum('Qty')).order_by('-sales')[0:num] # show product_id and sum the id's Qty
        print("top3", top3)
    else:
        return JsonResponse({"results": {"error_message": f"strategy {order_by} not implenmented."}})
    return JsonResponse({"results": list(top3)})
    
def ValidateAddOrder(post_data,):
    print("validate add order")
    required_fields = ['pid', 'qty', 'is_vip', 'cid']
    p = Product.objects.get(id=post_data['pid'])
    for field in required_fields:
        if field not in post_data.keys():
            raise ValidationError(json.dumps({"error_message": f"field {field} is required."}))
    for k,v in post_data.items():
        if  k != "is_vip" and not v:
            raise ValidationError(json.dumps({"error_message": f"value of {k} must not be empty."}))
    if not post_data['is_vip']:
        if p.Vip:
            raise ValidationError(json.dumps({"error_message": "vip-purchased only"}))
    if p.Stock_pcs < int(post_data['qty']):
        raise ValidationError(json.dumps({"error_message": "insufficient stock.", "current_stock": p.Stock_pcs}))
    print("AddOrder is all validated.")
        
