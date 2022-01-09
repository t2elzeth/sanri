from dataclasses import dataclass

from shop.models import BuyRequest, Car


@dataclass
class AddBuyRequestDTO:
    from_client_id: int
    car: Car


@dataclass
class ApproveBuyRequestDTO:
    request: BuyRequest


@dataclass
class DeclineBuyRequestDTO:
    request: BuyRequest
