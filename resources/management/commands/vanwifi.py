import csv
from dataclasses import dataclass, asdict
import logging
from django.conf import settings
from django.contrib.gis.geos import Point
from pathlib import Path
from typing import Any
from street_ninja_server.base_commands import StreetNinjaCommand
from resources.models import PublicWifi

logger = logging.getLogger(__file__)


@dataclass
class WifiData:
    ssid: str
    location: Point
    is_active: bool


class Command(StreetNinjaCommand):

    help = "Populate the PublicWifi table with VanWifi data from the CSV data at data/vanwifi.csv"

    def handle(self, *args, **kwargs):
        try:
            VanWifiCsvHandler.handle()
        except Exception as e:
            logger.error(f"{e.__class__.__name__}: {e}", exc_info=True)



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

    def extract_data(self) -> list[WifiData]:
        extracted_data = []
        with self.file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    point = self._get_point(row)
                except Exception as e:
                    logger.error(f"Skipping row due to unexpected {e.__class__.__name__}: {e}", exc_info=True)
                    self.skipped_rows += 1
                    continue
                data = WifiData(
                    ssid=row["SSID"],
                    location=point,
                    is_active=True if row["AP Status"] == "Active" else False
                )
                extracted_data.append(data)
        logger.info(f"Extracted rows: `{len(extracted_data)}`\tSkipped rows: `{self.skipped_rows}`")
        return extracted_data

    def save_data(self, data: list[WifiData]):
        active_records = [PublicWifi(**asdict(record)) for record in data if record.is_active == True]
        saved_records = PublicWifi.objects.bulk_create(active_records)
        logger.info(f"Saved `{len(saved_records)}` new PublicWifi records")


    def _get_point(self, row: dict[str, Any]) -> Point:
        lon = float(row["Longitude"])
        lat = float(row["Latitude"])
        return PublicWifi.get_point(lon=lon, lat=lat)


    def _file_path(self) -> Path:
        data_dir: Path = settings.BASE_DIR / "data"
        return data_dir / self.FILE_NAME

