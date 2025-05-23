import copy
import pytest
import random
from cache.redis.access_patterns.base_access_patterns import AccessPatternDB
from cache.dataclasses import PhoneSessionData
from cache.redis.clients.phone_session_client import PhoneSessionCacheClient
from cache.follow_up_caching_service import FollowUpCachingService
from .testdata_factories import generate_fake_phone_session_data, generate_fake_sms_inquiry
from street_ninja_server.tests.utils.helpers import all_access_patterns, generate_id_list


@pytest.mark.parametrize("ids", [generate_id_list(), None])
@pytest.mark.parametrize("resource_access_pattern", all_access_patterns())
def test_update_phone_session(
        resource_access_pattern: AccessPatternDB, 
        phone_session_cache_client: PhoneSessionCacheClient,
        ids: list[int] | None,
):
    
    test_phone_session = generate_fake_phone_session_data()
    service = FollowUpCachingService(
        inquiry=generate_fake_sms_inquiry(),
        session_cache_client=phone_session_cache_client,
        resource_access_pattern=resource_access_pattern,
        session_access_pattern=phone_session_cache_client.access_pattern,
    )
    updated_phone_session = service.update_phone_session(
        session_data=copy.deepcopy(test_phone_session),
        ids=ids,
    )
    
    assert isinstance(updated_phone_session, PhoneSessionData)
    assert updated_phone_session.last_updated > test_phone_session.last_updated
    
    fetched_session_data = service.get_phone_session()
    
    assert fetched_session_data.keyword == updated_phone_session.keyword
    assert fetched_session_data.inquiry_id == updated_phone_session.inquiry_id
    assert fetched_session_data.ids == updated_phone_session.ids
    assert fetched_session_data.last_updated == updated_phone_session.last_updated