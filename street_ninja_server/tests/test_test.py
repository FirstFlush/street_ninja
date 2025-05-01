import pytest
from resources.models import Shelter, FoodProgram, Toilet, DrinkingFountain

@pytest.mark.django_db
def test_test(client, preload_all_resources):


    print(Shelter.objects.all().count())
    print(FoodProgram.objects.all().count())
    print(DrinkingFountain.objects.all().count())
    print(Toilet.objects.all().count())