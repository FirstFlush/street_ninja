import random
from faker import Faker
from cache.dataclasses import PhoneSessionData
from sms.enums import SMSKeywordEnum


fake = Faker()

def generate_fake_phone_session_data() -> PhoneSessionData:
    return PhoneSessionData(
        last_updated=fake.date_time_between(start_date="-1h", end_date="now"),
        keyword=random.choice(SMSKeywordEnum.values),
        inquiry_id=random.randint(1, 10000),
        ids=random.sample(range(0, 200), k=random.randint(0, 100)),
        resource_params=None,
    )
