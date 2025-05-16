import pytest
from cache.dataclasses import PhoneSessionData
from cache.redis.clients.phone_session_client import PhoneSessionCacheClient
from .testdata_factories import generate_fake_phone_session_data


@pytest.mark.parametrize(
    "phone_session_data",
    [generate_fake_phone_session_data() for _ in range(0, 1)],
)
def test_set_phone_session_client(
    phone_session_cache_client: PhoneSessionCacheClient, 
    phone_session_data: PhoneSessionData
):
    phone_session_cache_client.set_session(phone_session_data)
    data_from_session = phone_session_cache_client.get_session()
    assert isinstance(data_from_session, PhoneSessionData)
    assert data_from_session.ids == phone_session_data.ids
    assert data_from_session.inquiry_id == phone_session_data.inquiry_id
    assert data_from_session.keyword == phone_session_data.keyword
    assert data_from_session.resource_params == phone_session_data.resource_params