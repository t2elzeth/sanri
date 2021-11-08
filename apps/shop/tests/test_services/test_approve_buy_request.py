from django.test import TestCase

from shop.dto.buy_request import ApproveBuyRequestDTO
from shop.models import BuyRequest
from shop.models_factory import BuyRequestFactory
from shop.services.buy_request import ApproveBuyRequestService


class TestApproveBuyRequestService(TestCase):
    def setUp(self) -> None:
        self.req: BuyRequest = BuyRequestFactory.create()
        data = ApproveBuyRequestDTO(request_id=1)
        self.service = ApproveBuyRequestService(data=data)

    def test_get_request_instance(self):
        req = self.service._get_request_instance()

        self.assertIsInstance(req, BuyRequest)
        self.assertEqual(req.id, 1)

    def test_set_approve_field(self):
        res = self.service._set_approve_field(self.req)

        self.assertIsNone(res)
        self.assertEqual(self.req.approved, True)

    def test_execute(self):
        req = self.service.execute()

        self.assertIsInstance(req, BuyRequest)
