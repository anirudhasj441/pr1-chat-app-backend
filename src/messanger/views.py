from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.db.models import Q
from authenticator.serializers import userSerializer
import time

User = get_user_model()

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
    
class search(APIView):

    def post(self, request):

        data = request.data
        s = data["s"]
        result = User.objects.filter(
            Q(username__icontains =  s)|
            Q(first_name__icontains = s)|
            Q(last_name__icontains = s)
        )
        serializer = userSerializer(result, many=True)

        return Response(serializer.data)

