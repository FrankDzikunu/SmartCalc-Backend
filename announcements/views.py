# announcements/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Announcement
from .serializers import AnnouncementSerializer

@api_view(["GET"])
def get_active_announcement(request):
    announcement = Announcement.objects.filter(active=True).order_by("-created_at").first()

    if not announcement:
        return Response({"message": None}, status=200)

    serializer = AnnouncementSerializer(announcement)
    return Response(serializer.data, status=200)
