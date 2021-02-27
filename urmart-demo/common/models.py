from django.db import models

# Create your models here.

class Product(models.Model):
    id           = models.AutoField(primary_key=True)
    Stock_pcs    = models.IntegerField(default=0)
    Price        = models.IntegerField(blank=False)
    Shop_id      = models.ForeignKey("Shop", on_delete=models.CASCADE)
    Vip          = models.BooleanField(default=0)
    CreatedTime  = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = "Product"

class Shop(models.Model):
    Shop_id      = models.CharField(primary_key=True, max_length=2)
    Name         = models.CharField(max_length=50, blank=False)
    CreatedTime  = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = "Shop"

class Order(models.Model):
    id           = models.AutoField(primary_key=True)
    Product_id   = models.ForeignKey("Product", on_delete=models.CASCADE)
    Qty          = models.IntegerField(default=1)
    Price        = models.IntegerField(blank=False)
    Shop_id      = models.CharField(max_length=50, blank=False)
    Customer     = models.CharField(max_length=50, blank=False)
    CreatedTime  = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = "Order"


class ScheduleLog(models.Model):
    id           = models.AutoField(primary_key=True)
    FuncName     = models.CharField(max_length=50, blank=False)
    is_sent      = models.BooleanField(default=0)
    To           = models.TextField(blank=False)
    Comment      = models.TextField(blank=True)
    CreatedTime  = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = "ScheduleLog"
