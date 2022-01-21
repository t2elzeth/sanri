from django.test import TestCase
from shop.dto.buy_request import ApproveBuyRequestDTO
from shop.models import BuyRequest, Car
from shop.models_factory import BuyRequestFactory, CarFactory
from shop.services.buy_request import ApproveBuyRequestService


class TestApproveBuyRequestService(TestCase):
    def setUp(self) -> None:
        self.car: Car = CarFactory.create()
        self.req: BuyRequest = BuyRequestFactory.create(car=self.car)
        data = ApproveBuyRequestDTO(request=self.req)
        self.service = ApproveBuyRequestService(data=data)

    def test_get_request_instance(self):
        req = self.service._get_request_instance()

        self.assertIsInstance(req, BuyRequest)
        self.assertEqual(req.id, 1)

    def test_set_approve_field(self):
        res = self.service._set_approve_field(self.req)

        self.assertIsNone(res)
        self.assertEqual(self.req.status, BuyRequest.STATUS_APPROVED)

    def test_decline_other_requests(self):
        BuyRequestFactory.create(car=self.car)
        BuyRequestFactory.create(car=self.car)
        BuyRequestFactory.create(car=self.car)
        BuyRequestFactory.create(car=self.car)
        BuyRequestFactory.create(car=CarFactory.create())
        BuyRequestFactory.create()

        res = self.service._decline_other_requests(self.req)

        self.assertIsNone(res)
        for req in (
            BuyRequest.objects.exclude(id=self.req.id)
            .filter(car__id=self.req.car.id)
            .values("status")
        ):
            self.assertEqual(req["status"], BuyRequest.STATUS_DECLINED)

    def test_set_car_sold_status(self):
        res = self.service._set_car_sold_status(self.req)

        self.assertIsNone(res)
        self.assertEqual(self.req.car.sold, True)

    def test_execute(self):
        req = self.service.execute()

        self.assertIsInstance(req, BuyRequest)
