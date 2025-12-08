# announcements/admin.py
from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "created_at", "updated_at")
    list_filter = ("active", "created_at")
    search_fields = ("title", "message")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("title", "message", "link", "active")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = ("created_at", "updated_at")
