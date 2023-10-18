from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

# Create your views here.

class index(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        channel_layer = get_channel_layer()
        print(channel_layer)
        print("hello")
        for i in range(10):
            async_to_sync(channel_layer.group_send)(
                'test_consumer', {
                    'type': 'sendCounter',
                    'values': i
                }
            )
            time.sleep(1)
        return Response({'status': 200, 'message': "Hello World!"})
