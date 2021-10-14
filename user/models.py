from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, blank = True, null = True,)
    username = models.CharField(max_length = 200, blank = True, null = True,)
    image = models.ImageField(blank = True, null = True, upload_to = 'static/profile', default='profile/user-default.png')
    email = models.EmailField(blank=True, null=True, default='devsearch@email.com')
    profession = models.CharField(max_length = 500, blank = True, null = True,)
    bio  = models.TextField(blank = True, null = True,)
    social_linkedin = models.CharField(max_length = 2000, blank = True, null = True,)
    social_website= models.CharField(max_length = 2000, blank = True, null = True,)
    created = models.DateTimeField(auto_now_add = True)
    id = models. UUIDField(default = uuid.uuid4, editable = False, primary_key = True, unique = True)
    location = models.CharField(max_length = 200, blank = True, null = True,)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, default = '',  blank = True, null = True,)
    about = models.TextField(default = "About Skills", blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True)
    id = models. UUIDField(default = uuid.uuid4, editable = False, primary_key = True, unique = True)

    def __str__(self):
        return self.name

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, email=instance.email)

# @receiver(post_save, sender=Profile)
# def UpdateProfile(sender, instance, created, **kwargs):
#     profile = instance
#     user = profile.user
#     if created == False:
#         user.username = profile.username
#         user.save()

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True, blank=True)
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True, blank=True, related_name = 'allmessages')
    name = models.CharField(max_length=2000)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, editable = False, primary_key = True, unique = True)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['-created']

        
        
        
