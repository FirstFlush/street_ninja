from datetime import datetime, timedelta
import random
from faker import Faker
from cache.dataclasses import PhoneSessionData
from sms.enums import SMSKeywordEnum


fake = Faker()


KEYWORDS = SMSKeywordEnum.values

def generate_fake_phone_session_data() -> PhoneSessionData:
    return PhoneSessionData(
        last_updated=fake.date_time_between(start_date="-1h", end_date="now"),
        keyword=random.choice(KEYWORDS),
        inquiry_id=random.randint(1, 1000),
        ids=random.sample(range(0,100), k=random.randint(4, 25)),
        resource_params=None,
    )