from django.urls import path
from .views import CreateUserView, UserListView, MeView, ChangePasswordView, BulkCreateUserView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('bulk-create/', BulkCreateUserView.as_view(), name='bulk_create_users'),
    path('list/', UserListView.as_view(), name='list_users'),
    path('me/', MeView.as_view(), name='me'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
