# models.py (or in a utils.py if preferred)

from django.contrib.auth.models import User
from django.db.models import Q
from .models import Friendship

def get_friends(user):
    friends = Friendship.objects.filter(Q(user=user) | Q(friend=user))
    friends_list = [f.friend for f in friends if f.user == user] + [f.user for f in friends if f.friend == user]
    return friends_list

User.add_to_class('friends', get_friends)
