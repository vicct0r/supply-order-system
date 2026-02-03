from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, OrderCreationSerializer, OrderOperationalChoiceSerializer, OrderChoiceSerializer, InsufficientBatchQtyInfoSerializer
from catalog.models import Product
from hub.models import CD

# restrito
class OrderCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        _operation = False

        print(data)
        product = get_object_or_404(Product, sku=data['sku'])
        
        if product.quantity < data['quantity']:
            _status=Order.AWAITING_CUSTOMER_DECISION
        else:
            _status=Order.PENDING
            _operation=True

        order = Order.objects.create(
            product=product,
            client=data['client'],
            quantity=data['quantity'],
            total_price=product.price * data['quantity'],
            status=_status,
        )

        if _operation:
            response_serializer = OrderSerializer(order)
        else:
            response_serializer = InsufficientBatchQtyInfoSerializer(order)
        return Response(response_serializer.data)


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.exclude(status__in=[Order.COMPLETED, Order.REJECTED])


# restrito
class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'


# publico
class OrderRetrieveAPIView(APIView):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)

        if order.status == Order.AWAITING_CUSTOMER_DECISION:
            serializer = OrderOperationalChoiceSerializer(order)
        else:
            serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, id):
        serializer = OrderChoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choice = serializer.validated_data['choice']
        order = get_object_or_404(Order, id=id)
        response_serializer = OrderSerializer(order)

        # 0 -> proceed with available batch quantity
        # 1 -> wait for requested batch quantity

        if choice == 0:
            _status = Order.PENDING
            _operation = Order.CONFIRMED_CURRENT_BATCH_QUANTITY
        if choice == 1:
            _status = Order.PENDING
            _operation = Order.WAITED_FOR_REQUESTED_BATCH_QUANTITY
        
        order.status = _status
        order.operation = _operation
        order.save()
        return Response(response_serializer.data)
        

# batchOperationalChoice
# Endpoint para cliente aceitar lote com qtd atual ou esperar lote completo (será preciso fazer uso de datas)
# Somente o dono do Pedido poderá escolher a operação
