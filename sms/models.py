from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import (
    SMSKeywordEnum, 
    LanguageEnum, 
    InquiryStatusEnum, 
    LocationType
)


class PhoneNumber(models.Model):

    number = models.CharField(max_length=20, unique=True)
    last_active = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Inquiry(models.Model):

    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, choices=SMSKeywordEnum.choices)
    location = gis_models.PointField(srid=4326)
    location_text = models.CharField(max_length=256)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    status = models.CharField(max_length=16, choices=InquiryStatusEnum.choices)
    language = models.CharField(max_length=3, choices=LanguageEnum.choices)
    message = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"


class RejectedInquiry(models.Model):

    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Rejected inquiries"


class InquiryResponse(models.Model):

    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    inquiry = models.ForeignKey(to=Inquiry, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

