from rest_framework.views import APIView, Request, Response, status


class PingView(APIView):

    def get(self, request: Request, *args, **kwargs):
        return Response({"ping":"PONG"}, status=status.HTTP_200_OK)
