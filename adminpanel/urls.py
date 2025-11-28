from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('add-admin/', views.add_admin, name='add_admin'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
