import factory
import factory.fuzzy
from django.contrib.gis.geos import Point
from sms.models import SMSInquiry, SMSFollowUpInquiry, Conversation, Location
from sms.enums import SMSKeywordEnum, SMSFollowUpKeywordEnum
from geo.models import Location