from django.urls import path
from .views import CreateUserView, UserListView, MeView, ChangePasswordView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('list/', UserListView.as_view(), name='list_users'),
    path('me/', MeView.as_view(), name='me'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
