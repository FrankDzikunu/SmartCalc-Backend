from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        # Set staff/admin status
        user.is_staff = validated_data.get('is_staff', False)
        user.is_superuser = validated_data.get('is_superuser', False)
        user.save()

        return user

class CustomLoginSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        identifier = attrs.get("username")  # username OR email
        password = attrs.get("password")

        # Resolve email → username
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username/email or password")

        # REQUIRED for SimpleJWT
        self.user = user

        refresh = self.get_token(user)

        user_profile = getattr(user, 'userprofile', None)
        must_change_password = user_profile.must_change_password if user_profile else False
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "must_change_password": must_change_password,
        }
    