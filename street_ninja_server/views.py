from rest_framework.views import APIView, Request, Response, status


class PingView(APIView):

    def get(self, request: Request, *args, **kwargs):
        return Response({"ping":"PONG"}, status=status.HTTP_200_OK)


class ScratchView(APIView):

    def get(self, request: Request, *args, **kwargs):

        from cache.redis.clients.geo_client import NeighborhoodCacheClient

        cache_client = NeighborhoodCacheClient()
        hoods = cache_client.get_or_set_db()


        return Response({"bleh":1}, status=status.HTTP_200_OK)