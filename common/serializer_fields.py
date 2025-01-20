from typing import Any
from rest_framework import serializers


class YesNoBooleanField(serializers.Field):
    """
    Custom field to transform 'yes'/'no' to True/False
    Also transforms '?' and None/null to False
    """
    def to_internal_value(self, data: Any) -> bool:
        if data == None:
            return False
        elif not isinstance(data, str):
            raise serializers.ValidationError("Input must be a string.")
        
        data = data.strip().lower()
        match data:
            case "yes" | "y":
                return True
            case "no" | "n" | "?" | "":
                return False
            case _:
                raise serializers.ValidationError("Must be 'yes/y', 'no/n/?', or empty.")

    def to_representation(self, value: bool) -> str:
        if not isinstance(value, bool):
            raise TypeError("Expected a boolean value for representation.")
        return "yes" if value else "no"
