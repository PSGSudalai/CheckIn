from rest_framework import serializers
from apps.ACCESS.models import User
from rest_framework.authtoken.models import Token
from apps.BASE.serializers import ReadOnlySerializer, WriteOnlySerializer

class RegisterSerializer(serializers.ModelSerializer):
   
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "uuid",
            "identity",
            "phone_number",
            "password",
            "token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"detail": "User with this phone_number already exists."}
            )

        user = User(
            identity=validated_data.get("identity"),
            phone_number=validated_data.get("phone_number"),
            password=validated_data.get("password"),
        )
        user.save()
        return user


    # def get_access_token(self, obj):
    #     """Generate the access token for the user."""
    #     refresh = RefreshToken.for_user(obj)
    #     return str(refresh.access_token)

    # def get_refresh_token(self, obj):
    #     """Generate the refresh token for the user."""
    #     refresh = RefreshToken.for_user(obj)
    #     return str(refresh)


class UserListReadOnlySerializer(ReadOnlySerializer):
    class Meta(ReadOnlySerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "employee_id",
            "identity",
            "phone_number",
            "is_active",
        ]



class UserWriteOnlySerializer(WriteOnlySerializer):
    class Meta(WriteOnlySerializer.Meta):
        model = User
        fields = [
            "employee_id",
            "identity",
            "phone_number",
            "is_active",
        ]


class UserDetailSerializer(ReadOnlySerializer):
    
    class Meta(ReadOnlySerializer.Meta):
        model = User
        fields = [
            "id",
            "uuid",
            "email",
            "identity",
            "phone_number",
            "is_active",
        ]

