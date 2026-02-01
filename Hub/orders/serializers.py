from rest_framework import serializers

from .models import Order
from catalog.models import Product
from hub.models import CD


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified', 'status', 'client']


class OrderCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['sku', 'quantity', 'client']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('batch quantity must be greater than 1.')
        if value > 1000:
            raise serializers.ValidationError('batch request quantity limit reached max.: 1000.')
    
    def validate_sku(self, value):
        if len(value) > 10:
            raise serializers.ValidationError('Incorret SKU value format.')
        if len(value) < 7:
            raise serializers.ValidationError('Incorrect SKU value format.')


class BatchOperationalChoice(serializers.Serializer):
    class Meta:
        model = Order
        fields = ['operation']
