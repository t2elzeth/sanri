from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from authorization.models import User
from container.models import Container, CountAndSum

class CreateContainerTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('container-list-create')
        self.container_client = User.objects.create_user(
            password="123",
            fullName="My owner client",
            country="KG",
            email="oldClient@gmail.com",
            phoneNumber="+996771221103",
            service=User.SERVICE_ENTIRE,
            atWhatPrice=User.AT_WHAT_PRICE_BY_FACT,
            username="owner_client",
        )

    def test_container_create_with_valid_data(self):
        payload = {
            'client_id': self.container_client.id,
            'name': 'My test container',
            'dateOfSending': '2003-11-22',
            'commission': 2500,
            'containerTransportation': 2500,
            'packagingMaterials': 2500,
            'transportation': 2000,
            'loading': 2000,
            'wheelRecycling': {
                'count': 25,
                'sum': 200
            },
            'wheelSales': {
                'count': 20,
                'sum': 2000
            },
            'status': Container.STATUS_GOING_TO,
            'totalAmount': 2000
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        container = Container.objects.get(id=response.data['id'])
        wheel_recycling = CountAndSum.objects.filter(container=container).first()
        wheel_sales = CountAndSum.objects.filter(container=container).last()
        self.assertEqual(wheel_recycling.count, 25)
        self.assertEqual(wheel_recycling.sum, 200)
        self.assertEqual(wheel_sales.count, 20)
        self.assertEqual(wheel_sales.sum, 2000)
