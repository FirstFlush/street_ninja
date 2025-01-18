from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class RequestData:
    method: str
    endpoint: str
    headers: Optional[dict[str, str] | None] = None
    params: Optional[dict[str, str] | None] = None
    data: Optional[dict[str, str] | None] = None

    def to_request_dict(self) -> dict[str, str]:
        """Used to pass RequestData attributes to requests.request() as kwargs."""
        d = asdict(self)
        d.pop('endpoint')
        return {key: value for key, value in d.items() if value is not None}