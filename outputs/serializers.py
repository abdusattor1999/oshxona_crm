from rest_framework import serializers
from .models import *
from accounts.serializers import KitchenEditSerializer

class OutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Output
        fields = 'id', 'name', 'kitchen_id', 'description', 'is_product', 'get_cost'
        read_only_fields = 'id', 'get_cost'


class OutputItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputItem
        fields = "id", "output_id", "product", "description", "amount", "price"