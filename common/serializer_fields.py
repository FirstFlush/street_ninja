from typing import Any
from rest_framework import serializers
from decimal import Decimal


# class FlexibleDecimalField(serializers.Field):
#     """
#     Custom field to transform columns with strings such as "$10.00" or "Free"
#     into standardized decimal formats.
#     """
#     def to_internal_value(self, data: Any) -> Decimal:
#         if isinstance(data, (Decimal, int, float)):
#             return Decimal(data)
#         elif not isinstance(data, str):
#             raise serializers.ValidationError("Input must be a string or number.")

#         normalized_str = 


class YesNoBooleanField(serializers.Field):
    """
    Custom field to transform 'yes'/'no' to True/False
    Also transforms '?' and None/null to False
    """
    def to_internal_value(self, data: Any) -> bool:
        if data is None:
            return False
        elif data is True:
            return True
        elif data is False:
            return False
        elif not isinstance(data, str):
            raise serializers.ValidationError("Input must be a string.")
        
        data = data.strip().lower()
        match data:
            case "yes" | "y" | "true":
                return True
            case "no" | "n" | "?" | "false" | "" | "unknown":
                return False
            case _:
                raise serializers.ValidationError("Must be 'yes/y', 'no/n/?', or empty.")

    def to_representation(self, value: bool) -> str:
        if not isinstance(value, bool):
            raise TypeError("Expected a boolean value for representation.")
        return "yes" if value else "no"
