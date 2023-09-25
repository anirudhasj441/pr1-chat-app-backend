from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authenticator.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'dob', 'profile_pic',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'dob', 'profile_pic',)