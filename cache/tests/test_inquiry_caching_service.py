from datetime import datetime
import pytest
from typing import Type
from cache.dataclasses import PhoneSessionData
from cache.inquiry_caching_service import InquiryCachingService
from cache.redis.clients import PhoneSessionCacheClient
from cache.redis.access_patterns.base_access_patterns import AccessPatternDB
from street_ninja_server.global_mappings import ACCESS_PATTERN_TO_MODEL
from .testdata_factories import generate_fake_sms_inquiry, generate_id_list


def _access_patterns() -> list[Type[AccessPatternDB]]:
    return list(ACCESS_PATTERN_TO_MODEL.keys())


@pytest.mark.parametrize("resource_access_pattern", _access_patterns())
def test_inquiry_caching_service(
        resource_access_pattern: Type[AccessPatternDB], 
        phone_session_cache_client: PhoneSessionCacheClient
):
    test_sms_inquiry = generate_fake_sms_inquiry()
    service = InquiryCachingService(
        inquiry=test_sms_inquiry,
        session_cache_client=phone_session_cache_client,
        resource_access_pattern=resource_access_pattern,
        session_access_pattern=phone_session_cache_client.access_pattern,
    )
    generated_ids = generate_id_list()
    phone_session = service.create_phone_session(
        ids=generated_ids,
    )
    time_created = phone_session.last_updated
    
    assert isinstance(phone_session, PhoneSessionData)
    assert phone_session.ids == generated_ids
    assert phone_session.keyword == test_sms_inquiry.keyword
    assert phone_session.inquiry_id == test_sms_inquiry.id
    
    new_ids = generate_id_list()[:4]
    updated_phone_session = service.update_phone_session(
        session_data=phone_session,
        ids=new_ids,
    )
    
    assert isinstance(updated_phone_session, PhoneSessionData)
    assert updated_phone_session.ids == new_ids
    assert updated_phone_session.keyword == test_sms_inquiry.keyword
    assert updated_phone_session.inquiry_id == test_sms_inquiry.id
    assert updated_phone_session.last_updated > time_created