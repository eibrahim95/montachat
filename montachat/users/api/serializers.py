from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
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
    name = CharField(
        allow_blank=False,
        label="Name of User",
        max_length=255,
        required=True,
    )

    def save(self, request):
        user = super().save(request)
        user.name = self.validated_data["name"]
        user.save()
        return user


class MontaLoginSerializer(LoginSerializer):
    username = None


class MontaUserDetailsSerializer(UserDetailsSerializer):
    name = CharField(
        allow_blank=False,
        label="Name of User",
        max_length=255,
        required=True,
    )
    first_name = None
    last_name = None

    class Meta:
        model = User
        fields = ("name", "id", "email")
        read_only_fields = ("id", "email")
        write_only_fields = ("password",)
