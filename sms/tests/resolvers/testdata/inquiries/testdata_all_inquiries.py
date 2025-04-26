from .testdata_food import FOOD_INQUIRIES
from .testdata_shelter import SHELTER_INQUIRIES
from .testdata_water import WATER_INQUIRIES
from .testdata_toilet import TOILET_INQUIRIES
from .testdata_wifi import WIFI_INQUIRIES

from .testdata_shelter_params import SHELTER_PARAMS_INQUIRIES
from .testdata_food_params import FOOD_PARAMS_INQUIRIES

ALL_INQUIRIES = (
    FOOD_INQUIRIES +
    SHELTER_INQUIRIES +
    WATER_INQUIRIES +
    TOILET_INQUIRIES +
    WIFI_INQUIRIES +

    SHELTER_PARAMS_INQUIRIES +
    FOOD_PARAMS_INQUIRIES
)