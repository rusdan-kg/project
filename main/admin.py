from django.contrib import admin
from main.models import Product, Category, ConfirmCode

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ConfirmCode)