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


@pytest.mark.django_db
@pytest.mark.parametrize("enum_model_mapping", SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL.items())
def test_map_pin_view(preload_all_resources, enum_model_mapping: tuple[SMSKeywordEnum, ResourceModel], api_client: APIClient):
    
    keyword_lower = enum_model_mapping[0].value.lower()
    resource_model = enum_model_mapping[1]
    first = resource_model.objects.filter(is_active=True).first()
    if first:
        id = first.id
        response: Response = api_client.get(
            path=reverse("map_pin", kwargs={
                "resourceType": keyword_lower,
                "id": id,
            } ),
        )
    
        assert response.status_code == 200