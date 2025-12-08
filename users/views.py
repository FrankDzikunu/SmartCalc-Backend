from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import CustomLoginSerializer


class IsAdmin(permissions.BasePermission):
    """Allow only admin users."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class CreateUserView(generics.CreateAPIView):
    """
    Admin-only endpoint for creating new users.
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class UserListView(generics.ListAPIView):
    """
    Admin-only list of all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class MeView(APIView):
    """
    Returns info of the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        # this Convert JWT response to mobile app format
        return Response({
            "token": data.get("access"),
            "refresh": data.get("refresh")
        })