from django.db import models
from common.enums import SMSKeyword


class PhoneNumber(models.Model):

    number = models.CharField(max_length=20, unique=True)
    last_active = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Inquiry(models.Model):

    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    status = models.CharField(max_length=16)
    message = models.CharField(max_length=256)
    keyword = models.CharField(max_length=20, choices=SMSKeyword.choices)
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

