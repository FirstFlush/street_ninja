from common.base_enum import StreetNinjaEnum
import csv
from dataclasses import dataclass, asdict, field
import logging
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import transaction
from pathlib import Path
import re
from typing import Any, Optional
from street_ninja_server.base_commands import StreetNinjaCommand
from resources.models import PublicWifi


logger = logging.getLogger(__name__)


class ValidSSID(StreetNinjaEnum):
    COV_PUBLIC = "CoV_Public"
    VAN_WIFI = "#VanWiFi"
    VPL = "VPL"


@dataclass
class WifiData:
    ssid: str
    location: Point
    is_active: bool
    name: Optional[str] = field(default="")
    address: Optional[str] = field(default="")


class Command(StreetNinjaCommand):

    help = "Populate the PublicWifi table with VanWifi data from the CSV data at data/vanwifi.csv"

    def handle(self, *args, **kwargs):
        try:
            VanWifiCsvHandler.handle()
        except Exception as e:
            logger.error(f"{e.__class__.__name__}: {e}", exc_info=True)
            logger.error("Could not process vanwifi.csv file. Check error logs for details.")

class VanWifiCsvHandler:

    FILE_NAME = "vanwifi.csv"

    def __init__(self):
        self.file_path = self._file_path()  
        self.skipped_rows = 0
        
    @classmethod
    def handle(cls):
        handler = cls()
        csv_data = handler.extract_data()
        handler.save_data(csv_data)

    def _extract_name(self, row: dict[str, Any]) -> str:
        name: str = row.get("Site Name", "")
        if any([char.isalpha() for char in list(name)]):
            return name
        return ""

    def _is_junk_address(self, pattern: re.Pattern, s: str) -> bool:
        """
        Returns True if the address is invalid based on known junk patterns in vanwifi.csv.

        Specifically catches:
        - Technician placement notes like "18' W side", "14' N side", etc.
        - Nonsense or placeholder entries under 4 characters like "X1", "X2", etc.

        These are not real addresses and should be excluded from parsed results.
        """
        return bool(re.match(pattern, s.strip()) or len(s) < 5)

    def _extract_ssid(self, row: dict[str, Any]) -> str:
        ssid = row["SSID"]
        try:
            enum = ValidSSID(ssid)
        except ValueError:
            if ssid == "CoV Premises":
                enum = ValidSSID.COV_PUBLIC
            else:
                enum = ValidSSID.VAN_WIFI
        return enum.value


    def _extract_address(self, row: dict[str, Any]) -> str:
        pattern = re.compile(r"^\d{1,2}' [NSEW] side$")
        address: str = row.get("Address", "")
        if address and any([char.isalpha() for char in list(address)]):
            if not self._is_junk_address(pattern, address):
                return address.strip()
        return ""

    def extract_data(self) -> list[WifiData]:
        extracted_data = []
        with self.file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    point = self._get_point(row)
                except Exception as e:
                    logger.warning(f"Skipping row due to unexpected {e.__class__.__name__}: {e}")
                    self.skipped_rows += 1
                    continue
                data = WifiData(
                    name=self._extract_name(row),
                    address=self._extract_address(row),
                    ssid=self._extract_ssid(row),
                    location=point,
                    is_active=True if row["AP Status"] == "Active" else False
                )
                extracted_data.append(data)
        logger.info(f"Extracted rows: `{len(extracted_data)}`\tSkipped rows: `{self.skipped_rows}`")
        return extracted_data

    def save_data(self, data: list[WifiData]) -> list[PublicWifi]:
        saved_records = []
        with transaction.atomic():
            for record in data:
                instance = PublicWifi.objects.get_or_create(**asdict(record))
                saved_records.append(instance)
        logger.info(f"Saved `{len(saved_records)}` new PublicWifi records")
        return saved_records

    def _get_point(self, row: dict[str, Any]) -> Point:
        lon = float(row["Longitude"])
        lat = float(row["Latitude"])
        return PublicWifi.get_point(lon=lon, lat=lat)


    def _file_path(self) -> Path:
        data_dir: Path = settings.BASE_DIR / "data"
        return data_dir / self.FILE_NAME

