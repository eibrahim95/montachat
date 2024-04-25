from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.fields import CharField

from montachat.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class MontaRegisterSerializer(RegisterSerializer):
    username = None
    name = CharField(allow_blank=False, label='Name of User', max_length=255, required=True)

    def get_cleaned_data(self):
        print("Cleaning")
        return {
            **super().get_cleaned_data(),
            'name': self.validated_data.get('name', ''),
        }
