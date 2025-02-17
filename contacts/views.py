import logging
from django.db.utils import IntegrityError
from rest_framework.views import APIView, Response, Request, status
from .serializers import ContactSerializer
from .models import Contact


logger = logging.getLogger(__name__)


class ContactView(APIView):

    def post(self, request: Request, *args, **kwargs):
        http_status = status.HTTP_400_BAD_REQUEST 
        deserializer = ContactSerializer(data=request.data)
        if deserializer.is_valid():
            try:
                Contact.objects.create(**deserializer.validated_data)
            except IntegrityError as e:
                msg = f"Database error `{e.__class__.__name__} occurred while saving deserialized `{deserializer.__class__.__name__}` data: {e}`"
                logger.error(msg, exc_info=True)
            else:
                http_status = status.HTTP_201_CREATED
        else:
            msg = f"Deserialization of `{deserializer.__class__.__name__}` data failed. Deserialization errors: {deserializer.errors}"
            logger.error(msg)

        return Response({"success": True}, status=http_status)
