# announcements/models.py
from django.db import models

class Announcement(models.Model):
    """
    A simple announcement message that the mobile app will fetch.
    """
    title = models.CharField(max_length=200, blank=True)
    message = models.TextField(help_text="The message to display in the app.")
    link = models.URLField(
        blank=True,
        help_text="Link to app update (Play Store / App Store / direct)."
    )
    active = models.BooleanField(
        default=True,
        help_text="If true the mobile app should display this announcement."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return f"{self.title or self.message[:40]}{' (active)' if self.active else ''}"

    @classmethod
    def latest_active(cls):
        """
        Returns the latest active Announcement or None.
        """
        return cls.objects.filter(active=True).order_by('-created_at').first()
