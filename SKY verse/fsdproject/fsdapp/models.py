from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
# models.py

from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    link = models.URLField(max_length=900, null=True, blank=True) 
    image = models.ImageField(upload_to='posts/images', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos', null=True, blank=True)
    media_tag = models.CharField(max_length=50, choices=[('image', 'Image'), ('video', 'Video')], default='image')
    category = models.CharField(max_length=50, choices=[
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('job', 'Job'),
        ('news', 'News'),
        ('shopping', 'Shopping'),
        ('mixed', 'Mixed'),
        ('friends', 'Friends'), 
        ('kids', 'Kids')
    ], default='entertainment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.author.username}'

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"



class ECommerceIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_url = models.URLField()
    product_name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
# models.py

from django.db import models
from django.contrib.auth.models import User

# fsdapp/models.py

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile.jpg')
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.user.username
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    def __str__(self):
        return f"{self.from_user} to {self.to_user} ({self.status})"

    def accept(self):
        self.accepted = True
        self.save()

    def ignore(self):
        self.ignored = True
        self.save()

class FriendSuggestion(models.Model):
    user = models.ForeignKey(User, related_name='friend_suggestions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

from django.db import models
from django.contrib.auth.models import User

class UserFriendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('from_user', 'to_user')


