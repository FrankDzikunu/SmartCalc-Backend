from django.contrib import admin
from django.urls import path, include    
from users.views import CustomLoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # JWT Auth
    path('api/login/', CustomLoginView.as_view(), name='custom_token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users app
    path('api/users/', include('users.urls')),
    path('', include('adminpanel.urls')),

    # Announcements app
    path('api/announcements/', include('announcements.urls')),
]
