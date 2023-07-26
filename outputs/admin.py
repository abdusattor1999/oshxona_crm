from django.contrib import admin
from .models import Output, OutputItem
# Register your models here.

@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ["name", "kitchen", "is_product", "get_cost"]
    list_editable = ['is_product']
    list_filter = 'name', 'kitchen', 'is_product'

@admin.register(OutputItem)
class OutputAdmin(admin.ModelAdmin):
    list_display = ["product", "output", "description", "amount", "price"]
    list_filter = 'price', 'amount', 'output', 'product'

    