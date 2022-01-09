from shop.dto.buy_request import ApproveBuyRequestDTO
from shop.models import BuyRequest


class ApproveBuyRequestService:
    def __init__(self, data: ApproveBuyRequestDTO):
        self._data = data

    def _get_request_instance(self):
        return self._data.request

    def _set_approve_field(self, req: BuyRequest) -> None:
        req.status = BuyRequest.STATUS_APPROVED
        req.save()

    def _decline_other_requests(self, req: BuyRequest):
        BuyRequest.objects.exclude(id=req.id).filter(
            car__id=req.car.id
        ).update(status=BuyRequest.STATUS_DECLINED)

    def _set_car_sold_status(self, req: BuyRequest):
        req.car.sold = True
        req.car.save()

    def execute(self) -> BuyRequest:
        req = self._get_request_instance()
        self._set_approve_field(req)
        self._decline_other_requests(req)
        self._set_car_sold_status(req)

        return req
