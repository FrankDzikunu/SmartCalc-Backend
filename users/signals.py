from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Ensure the user is active
        if instance.is_active is False:
            instance.is_active = True
            instance.save(update_fields=['is_active'])
        
        # Make sure the password is hashed
        if not instance.password.startswith('pbkdf2_'):
            raw_password = instance.password
            instance.set_password(raw_password)
            instance.save(update_fields=['password'])

        # Create the UserProfile
        UserProfile.objects.create(user=instance)
