import logging
from django.http import HttpRequest
from rest_framework.views import APIView, Request, Response

logger = logging.getLogger(__name__)

class HomeView(APIView):


    def get(self, request:Request, *args, **kwargs):
        logger.critical("hihihihi")
        request._request.session['test_data'] = 'bleh'
        request._request.session.modified = True
        print(request._request.session.session_key)

        return Response({"ok":"good"})
