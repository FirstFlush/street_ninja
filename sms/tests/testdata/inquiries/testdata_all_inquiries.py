from .testdata_food import FOOD_INQUIRIES
from .testdata_shelter import SHELTER_INQUIRIES
from .testdata_water import WATER_INQUIRIES
from .testdata_toilet import TOILET_INQUIRIES
from .testdata_wifi import WIFI_INQUIRIES

from .testdata_shelter_params import SHELTER_PARAMS_INQUIRIES
from .testdata_food_params import FOOD_PARAMS_INQUIRIES
from .testdata_water_params import WATER_PARAMS_INQUIRIES
from .testdata_toilet_params import TOILET_PARAMS_INQUIRIES

from .testdata_neighborhoods import NEIGHBORHOOD_INQUIRIES_SIMPLE, NEIGHBORHOOD_INQUIRIES_INVALID


ALL_INQUIRIES = (
    FOOD_INQUIRIES +
    SHELTER_INQUIRIES +
    WATER_INQUIRIES +
    TOILET_INQUIRIES +
    WIFI_INQUIRIES +

    SHELTER_PARAMS_INQUIRIES +
    FOOD_PARAMS_INQUIRIES +
    WATER_PARAMS_INQUIRIES +
    TOILET_PARAMS_INQUIRIES +
    
    NEIGHBORHOOD_INQUIRIES_SIMPLE +
    NEIGHBORHOOD_INQUIRIES_INVALID
)
