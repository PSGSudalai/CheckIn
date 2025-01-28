from rest_framework import serializers
from apps.ACCESS.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.BASE.serializers import ReadOnlySerializer, WriteOnlySerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    access_token = serializers.SerializerMethodField(read_only=True)
    refresh_token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "employee_id",
            "password",
            "identity",
            "phone_number",
            "access_token",
            "refresh_token",
        ]
        extra_kwargs = {
            "phone_number": {"required": True, "max_length": 150},
            "identity": {"required": True},
        }

    def create(self, validated_data):
        """Create a new user and hash the password."""
        phone_number = validated_data.pop("phone_number")
        password = validated_data.pop("password")

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": "A user with this phone_number already exists."}
            )

        user = User.objects.create_user(phone_number=phone_number, **validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_access_token(self, obj):
        """Generate the access token for the user."""
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh_token(self, obj):
        """Generate the refresh token for the user."""
        refresh = RefreshToken.for_user(obj)
        return str(refresh)


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
            "email",
            "identity",
            "phone_number",
            "email",
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

