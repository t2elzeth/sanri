from dataclasses import dataclass


@dataclass
class AddBuyRequestDTO:
    from_client_id: int
    car_id: int


@dataclass
class ApproveBuyRequestDTO:
    request_id: int


@dataclass
class DeclineBuyRequestDTO:
    request_id: int
