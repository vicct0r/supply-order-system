from rest_framework import serializers

from .models import Order
from catalog.models import Product
from hub.models import CD


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    operation = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified', 'status', 'client']

    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_operation(self, obj):
        return obj.get_operation_display()


class OrderOperationalChoiceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.SerializerMethodField()
    available_quantity = serializers.IntegerField(source='product.quantity')
    instructions = serializers.SerializerMethodField()
    choices = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_choices(self, obj):
        return [0, 1]
    
    def get_instructions(self, obj):
        return (
            "[0] - Wait for requested batch quantity.",
            "[1] - Proceed with available batch quantity"
        )
    

class OrderChoiceSerializer(serializers.Serializer):
    choice = serializers.ChoiceField(choices=[0, 1])


class InsufficientBatchQtyInfoSerializer(serializers.Serializer):
    result = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    order_url = serializers.SerializerMethodField()
    operation = serializers.SerializerMethodField()

    def get_info(self, obj):
        return "Insufficient batch quantity. Choose the operational proccess in order URL."

    def get_order_url(self, obj):
        return obj.get_absolute_url()

    def get_operation(self, obj):
        return "order_created"
    
    def get_result(self, obj):
        return "success"

    
class OrderCreationSerializer(serializers.ModelSerializer):
    sku = serializers.CharField()

    class Meta:
        model = Order
        fields = ['sku', 'quantity', 'client']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('batch quantity must be greater than 1.')
        if value > 1000:
            raise serializers.ValidationError('batch request quantity limit reached max.: 1000.')
        return value
    
    def validate_sku(self, value):
        if len(value) > 10:
            raise serializers.ValidationError('Incorret SKU value format.')
        if len(value) < 7:
            raise serializers.ValidationError('Incorrect SKU value format.')
        if not Product.objects.filter(sku=value.upper()).exists():
            raise serializers.ValidationError('SKU product not found.')
        return value.upper()


