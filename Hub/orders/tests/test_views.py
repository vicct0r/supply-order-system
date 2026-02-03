from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from hub.models import CD
from catalog.models import Product
from ..models import Order

class TestOrderOperationalFlow(APITestCase):
    def setUp(self):
        self.client_obj = CD.objects.create(
            name="cd-00-test",
            ip="127.0.0.1:4000",
            region="Brasil/GO"
        )

        self.product = Product.objects.create(
            sku="ABC1234",
            price=100,
            quantity=50
        )

    def test_customer_decision_wait(self):
        response = self.client.post(
            reverse("orders:order_create"),
            {
                "client": str(self.client_obj.id),
                "sku": "ABC1234",
                "quantity": 60
            },
            format="json"
        )

        assert response.status_code == 202

        order = Order.objects.get()
        assert order.status == Order.AWAITING_CUSTOMER_DECISION

        response_choice = self.client.post(
            reverse("orders:order_detail", args=[order.id]),
            {
                "choice": 0
            },
            format="json"
        )

        assert response_choice.status_code == 200

        order.refresh_from_db()
        
        assert order.status is not Order.AWAITING_CUSTOMER_DECISION
        assert order.operation == Order.CONFIRMED_CURRENT_BATCH_QUANTITY
