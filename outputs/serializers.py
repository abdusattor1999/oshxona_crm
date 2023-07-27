from rest_framework import serializers
from .models import *
from accounts.serializers import KitchenEditSerializer

class OutputItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutputItem
        fields = "id", "name","description","amount","price"
        read_only_fields = 'id',


class OutputSerializer(serializers.ModelSerializer):
    items = OutputItemSerializer(many=True)
    class Meta:
        model = Output
        fields = 'id', 'title', 'kitchen_id', 'description', 'is_product', 'items', 'get_cost'
        read_only_fields = 'id', 'get_cost'

