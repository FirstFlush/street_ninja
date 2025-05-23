import random
from faker import Faker
from cache.dataclasses import PhoneSessionData
from sms.enums import SMSKeywordEnum
from sms.models import SMSInquiry
from dataclasses import dataclass, field

fake = Faker()

@dataclass
class TestConversation:
    id: int

@dataclass
class TestSMSInquiry:
    id: int
    conversation: TestConversation
    keyword: str
    message: str
    params: dict = field(default_factory=dict)


def generate_fake_phone_session_data() -> PhoneSessionData:
    return PhoneSessionData(
        last_updated=fake.date_time_between(start_date="-1h", end_date="now"),
        keyword=random.choice(SMSKeywordEnum.values),
        inquiry_id=random.randint(1, 10000),
        ids=random.sample(range(0, 200), k=random.randint(0, 100)),
        resource_params=None,
    )


def generate_fake_sms_inquiry() -> TestSMSInquiry:
    return TestSMSInquiry(
        id=random.randint(1, 1000),
        conversation=TestConversation(id=random.randint(1, 1000)),
        keyword=random.choice(SMSKeywordEnum.values),
        message="".join([fake.random_lowercase_letter() for _ in range(random.randint(8, 25))]),
    )
    
def generate_id_list() -> list[int]:
    return [random.randint(1, 200) for _ in range (random.randint(3, 15))]