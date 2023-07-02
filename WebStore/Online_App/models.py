from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    points_earned = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AndroidApp(models.Model):
    # user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE,default=3)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='app_pictures/')
    category = models.CharField(max_length=100)
    link = models.URLField()
    points = models.IntegerField()

    def __str__(self):
        return self.name


class Screenshot(models.Model):
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    app = models.ForeignKey(AndroidApp, on_delete=models.CASCADE, null=True, default=None)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()
