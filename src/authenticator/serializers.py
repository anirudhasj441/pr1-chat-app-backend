from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.models import User

class userSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        required_fields = [
            'email',
            'first_name',
            'last_name'
        ]
        
        for field in required_fields:
            if field not in data.keys():
                raise ValidationError({field: f"{field} if required"})
            
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password=validated_data["password"]
        )
        return user
    

        