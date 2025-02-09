from dataclasses import dataclass


@dataclass
class SMSResponseData:
    msg: str
    ids: list[int]

    @property
    def offset(self) -> int:
        return len(self.ids)