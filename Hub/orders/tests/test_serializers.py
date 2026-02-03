from django.test import TestCase
from orders.serializers import OrderCreationSerializer, OrderChoiceSerializer
from hub.models import CD
from ..models import Order
from catalog.models import Product

class TestOrderCreationSerializer(TestCase):

    def test_order_creation_serializer_valid_data(self):
        client = CD.objects.create(
            name="cd-test-01",
            ip="127.0.0.1",
            region="Brasil/GO"
        )

        data = {
            "client": str(client.id),
            "sku": "ABC1234",
            "quantity": 100
        }

        serializer = OrderCreationSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["quantity"], 100)
        self.assertEqual(serializer.validated_data["sku"], "ABC1234")

    def test_order_choices_serializer(self):
        client = CD.objects.create(
            name="cd-test-01",
            ip="127.0.0.1",
            region="Brasil/GO"
        )

        product = Product.objects.create(
            name='razer RX Test',
            quantity=100,
            price=120.00,
            sku="OPP00BR"
        )
        
        order = Order.objects.create(
            product=product,
            client=client,
            quantity=101
        )

        data = {
            "choice": 0
        }

        serializer = OrderChoiceSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["choice"], 0)
