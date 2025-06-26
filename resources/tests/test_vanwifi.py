import pytest
from resources.management.commands.vanwifi import VanWifiCsvHandler, WifiData, ValidSSID


@pytest.mark.parametrize("extracted_data", VanWifiCsvHandler().extract_data())
def test_extract_vanwifi_data(extracted_data: WifiData):
    
    assert extracted_data.ssid in ValidSSID.values
    assert 49.0 < extracted_data.location.y < 50
    assert -123.8 < extracted_data.location.x < -121.0