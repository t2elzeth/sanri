from django.core.management.base import BaseCommand
from car_model.models import CarMark
marks = """
TOYOTA
NISSAN
MAZDA
MITSUBISHI
HONDA
SUZUKI
SUBARU
ISUZU
DAIHATSU
MITSUOKA
LEXUS
AUDI
BENTLEY
BMW
CADILLAC
CHEVROLET
CHRYSLER
CITROEN
DODGE
FERRARI
FIAT
FORD
GM
GMC
HINO
HUMMER
INFINITI
JAGUAR
JEEP
KAWASAKI
KOMATSU
LAND ROVER
LOTUS
MASERATI
MERCEDES BENZ
OPEL
PEUGEOT
PORSCHE
RENAULT
TADANO
TCM
TESLA
VOLKSWAGEN
VOLVO
YANMAR
"""

marks = [mark for mark in marks.split() if len(mark) > 1 ]


class Command(BaseCommand):
    def handle(self, *args, **options):
        counter = 0
        for mark in marks:
            car_mark, created = CarMark.objects.get_or_create(name=mark)

            if not created:
                print(f'Mark {car_mark.name} already exists')
                continue

            print(f'Created CarMark: {car_mark.name}')
            counter += 1

        print(f'Created {counter} marks in total')
