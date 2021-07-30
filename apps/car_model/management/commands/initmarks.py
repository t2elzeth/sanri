from django.core.management.base import BaseCommand
from car_model.models import CarMark

marks = """
TOYOTA
HONDA
NISSAN
SUBARU
AUDI
VOLKSWAGEN
MERCEDES BENZ
BMW
MAZDA
MITSUBISHI
SUZUKI
ISUZU
TADANO
TCM
YANMAR
DAIHATSU
MITSUOKA
KAWASAKI
KOMATSU
LEXUS
CHEVROLET
RENAULT
DODGE
FERRARI
FIAT
FORD
GMC
HINO
INFINITI
JEEP
OPEL
TESLA
VOLVO
FORKLIFT
"""

marks = [mark for mark in marks.split() if len(mark) > 1]


class Command(BaseCommand):
    def handle(self, *args, **options):
        counter = 0
        for mark in marks:
            car_mark, created = CarMark.objects.get_or_create(name=mark)

            if not created:
                print(f"Mark {car_mark.name} already exists")
                continue

            print(f"Created CarMark: {car_mark.name}")
            counter += 1

        print(f"Created {counter} marks in total")
