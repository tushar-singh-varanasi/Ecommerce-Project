from django.contrib import admin
from .models import Customer,Product,Cart,OrderPlaced
# Register your models here.
@admin.register(Customer)

class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)

class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderPlaced)

class OrderPlacedAdmin(admin.ModelAdmin):
    pass

