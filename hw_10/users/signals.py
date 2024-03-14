from pathlib import Path
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        pass


@receiver(pre_delete, sender=User)
def delete_avatar(sender, instance, **kwargs):
    try:
        profile = instance.profile
        avatar = profile.avatar
        field = Profile._meta.get_field("avatar")
        default_avatar_path = field.default.replace("/", "")  # Remove leading slash
        avatar_path = avatar.path
        if avatar_path != default_avatar_path and Path(avatar_path).exists():
            avatar.delete(save=False)
    except Profile.DoesNotExist:
        # Handle the case where the Profile has not been created yet
        pass
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred while deleting the avatar: {e}")
