from dataclasses import dataclass
from shop.models import Car


@dataclass
class AddBuyRequestDTO:
    from_client_id: int
    car: Car


@dataclass
class ApproveBuyRequestDTO:
    request_id: int


@dataclass
class DeclineBuyRequestDTO:
    request_id: int
