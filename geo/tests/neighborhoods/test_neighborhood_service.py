import pytest
from _pytest.monkeypatch import MonkeyPatch
from geo.neighborhoods.neighborhood_service import NeighborhoodService
from geo.models import Neighborhood
import json
import os
from typing import Any


def _fetch_neighborhood_data_monkeypatch(self) -> dict[str, Any]:
    testdata_full_path = os.path.join(os.path.dirname(__file__), "testdata_neighborhoods.json")
    with open(testdata_full_path, "r") as f:
        data = json.load(f)
    return data


def test_get_neighborhoods(monkeypatch: MonkeyPatch):
    
    monkeypatch.setattr(NeighborhoodService, "_fetch_neighborhood_data", _fetch_neighborhood_data_monkeypatch)

    ns = NeighborhoodService()
    hoods = ns.get_neighborhoods()

    assert len(hoods) == 22
    assert hoods[0].name == "Dunbar-Southlands"
    assert hoods[-1].name == "Victoria-Fraserview"


@pytest.mark.django_db
def test_set_neighborhoods(monkeypatch: MonkeyPatch):

    monkeypatch.setattr(NeighborhoodService, "_fetch_neighborhood_data", _fetch_neighborhood_data_monkeypatch)

    ns = NeighborhoodService()
    hoods = ns.get_neighborhoods()
    ns.save_neighborhoods(hoods)
    
    neighborhoods = Neighborhood.objects.all()
    assert neighborhoods.count() == 22
    assert neighborhoods.first().name == "Dunbar-Southlands"
    assert neighborhoods.last().name == "Victoria-Fraserview"
    