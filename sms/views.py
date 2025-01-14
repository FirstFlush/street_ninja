from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from geo.geocoding import GeocodingService

class SMSInquiryView(APIView):

    def post(self, request:Request, *args, **kwargs):

        geocoding_service = GeocodingService()
        location = geocoding_service.geocode(query="688 Abbott St, Vancouver, BC, Canada")
        print(location)
        return Response({'bleh':'blahhh'}, status=status.HTTP_200_OK)