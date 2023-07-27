from django.contrib import admin
from .models import Output, OutputItem
# Register your models here.

@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ["title", "kitchen", "is_product", "get_cost"]
    list_editable = ['is_product']
    list_filter = 'title', 'kitchen', 'is_product'

@admin.register(OutputItem)
class OutputAdmin(admin.ModelAdmin):
    list_display = ["name", "output", "description", "amount", "price"]
    list_filter = 'price', 'amount', 'output', 'name'

    