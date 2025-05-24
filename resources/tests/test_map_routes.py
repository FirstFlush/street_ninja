import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.urls import reverse 
from sms.enums import SMSKeywordEnum
from ..abstract_models import ResourceModel
from street_ninja_server.global_mappings import SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL

resources_lowercase = [s.lower() for s in SMSKeywordEnum.values]

@pytest.mark.django_db
def test_map_view(preload_all_resources, api_client: APIClient):
    response: Response = api_client.get(reverse("map"))
    resource_data = response.data["data"]["resources"]
    
    assert response.status_code == 200    
    assert response.data["success"] == True
    assert isinstance(resource_data, dict)
    
    for k, v in resource_data.items():
        assert k in resources_lowercase
        assert len(v) > 0
        

