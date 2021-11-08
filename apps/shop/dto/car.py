from dataclasses import dataclass


@dataclass
class AddCarDTO:
    model_id: int
    year: int
    volume: float
    mileage: float
    condition: int
    price: float
    description: str

