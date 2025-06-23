# from scripts._utils import setup_django
from resources.models import PublicWifi
import csv
from typing import Any
import logging
from pathlib import Path
# from django.conf import settings
import django
import os
logger = logging.getLogger(__name__)


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "street_ninja_server.settings")
    django.setup()


class VanWifiCsvHandler:

    FILE_NAME = "vanwifi.csv"

    def __init__(self):
        self.file_path = self._file_path()

    def extract_data(self):
        with self.file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(row)
        
    def save_data(self, data: dict[str, Any]):
        ...

    def _file_path(self) -> Path:
        # data_dir: Path = settings.BASE_DIR / "data"
        data_dir = Path(__file__).parent / "data"
        return data_dir / self.FILE_NAME

if __name__ == "__main__":
    setup_django()
    handler = VanWifiCsvHandler()
    handler.extract_data()