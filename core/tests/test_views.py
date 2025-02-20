from django.test import TestCase, Client
from django.urls import reverse
from core.models import Product
from accounts.models import CustomUser


class AddToCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@xptocom', password='testpass'
        )
        self.client.login(username="testuser", password="testpass")
        
        self.product = Product.objects.create(name="Test product", price=50.00)

    def test_add_to_cart(self):
        response = self.client.get(reverse('add_to_cart'), {'id': self.product.id, 'quantity': 2})

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['qty_total_products'], 2)


class UpdateCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@xptocom', password='testpass'
        )
        self.client.login(username="testuser", password="testpass")

        self.product = Product.objects.create(name="Test product", price=50.00)

    def test_update_cart(self):
        response = self.client.get(reverse('update_cart'), {'id': self.product.id, 'quantity': 3})

        self.assertEqual(response.status_code, 200)

        data = response.json()
        # print(data)

        self.assertEqual(data['product']['id'], str(self.product.id))
        self.assertEqual(data['product']['subtotal'], '150.00')