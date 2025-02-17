from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from .serializers import ContactSerializer


class ContactView(APIView):

    def post(self, request: Request, *args, **kwargs):

        deserializer = ContactSerializer(data=request.data)
        if deserializer.is_valid():
            print(deserializer.validated_data)
        else:
            print(deserializer.errors)

        return Response("hi", status=status.HTTP_200_OK)
    