
from django.urls import path
from .views import get_active_announcement

urlpatterns = [
    path("active/", get_active_announcement, name="active-announcement"),
]
