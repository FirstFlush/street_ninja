import random
from faker import Faker
from common.utils import get_point
from django.contrib.gis.geos import Point

fake = Faker()


def generate_fake_location() -> tuple[str, Point]:
    lon = random.uniform(-123.22, 123.02)
    lat = random.uniform(49.20, 49.30)
    location_text = fake.street_address()
    return location_text, get_point(x=lon, y=lat)

def generate_bulk_fake_locations(n: int) -> list[tuple[str, Point]]:
    return [generate_fake_location() for i in range(0, n)]