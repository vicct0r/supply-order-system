from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Order
from .serializers import OrderSerializer, OrderCreationSerializer
from catalog.models import Product
from hub.models import CD

# restrito
class OrderCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_data = serializer.validated_data
        



# restrito
class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'

# publico
class OrderRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.exclude(status__in=[Order.COMPLETED, Order.REJECTED])
    lookup_field = 'id'


# batchOperationalChoice
# Endpoint para cliente aceitar lote com qtd atual ou esperar lote completo (será preciso fazer uso de datas)
# Somente o dono do Pedido poderá escolher a operação
