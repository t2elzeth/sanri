from dataclasses import dataclass
from shop.models import Car, BuyRequest


@dataclass
class AddBuyRequestDTO:
    from_client_id: int
    car: Car


@dataclass
class ApproveBuyRequestDTO:
    request: BuyRequest


@dataclass
class DeclineBuyRequestDTO:
    request_id: int
