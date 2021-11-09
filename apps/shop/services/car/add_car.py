from car_model.models import CarModel
from shop.models import Car
from shop.dto.car import AddCarDTO


class AddCarService:
    def __init__(self, data: AddCarDTO):
        self._data = data

    def _get_model(self) -> CarModel:
        return CarModel.objects.get(id=self._data.model_id)

    def execute(self) -> Car:
        model = self._get_model()

        car = Car.objects.create(
            model=model,
            year=self._data.year,
            volume=self._data.volume,
            mileage=self._data.mileage,
            condition=self._data.condition,
            price=self._data.price,
            description=self._data.description,
        )
        return car
