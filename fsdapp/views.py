from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, PostForm, EditProfileForm, ProfileForm, UserForm
from .models import Category, Post, Profile
from .forms import EditProfileForm, EditUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render
from .models import Profile, UserFriendship
from django.http import HttpResponseForbidden

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the author of the post can delete it
    if post.author == request.user:
        post.delete()
    
    return redirect('profile')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home') 
        else:
            messages.error(request, "There was an error with your registration. Please check the form.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})



@login_required
def profile(request):
    user = request.user
    # Ensure user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    # Fetch posts authored by the user
    posts = Post.objects.filter(author=user)

    context = {
        'user_form': UserForm(instance=user),
        'profile_form': EditProfileForm(instance=user.profile),
        'posts': posts,
    }

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Handle delete profile photo action
            if 'delete_profile_photo' in request.POST:
                user.profile.profile_photo.delete(save=False)  # Delete current profile photo without saving immediately
                user.profile.profile_photo = 'profile_photos/default_profile.jpg'  # Set default profile photo path
                user.profile.save()  # Save the profile with the default photo

            return redirect('profile')  # Redirect to profile page after saving changes

    return render(request, 'profile.html', context)
@login_required
def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    return render(request, 'profile.html', {'user_profile': profile})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Handle category-specific logic
            if post.category == 'friends':
                # Logic to display only on Friends page
                post.save()
                return redirect('profile')
            elif post.category == 'kids':
                # Logic to display only on Kids page
                post.save()
                return redirect('profile')
            else:
                # Display on both Friends home page and the selected category page
                post.save()
                return redirect('profile')  # Redirect to profile or appropriate page
            
        else:
            # Print form errors for debugging
            print(form.errors)
            return render(request, 'create_post.html', {'form': form})
            
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

@login_required
def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'view_post.html', {'post': post})

def logout_view(request):
    return render(request, 'logged_out.html')

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserForm
from .models import Profile

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'delete_profile_photo' in request.POST:
            if profile.profile_photo:
                profile.profile_photo.delete(save=False)
            profile.profile_photo = 'profile_photos/default_profile.jpg'  # Set to your default photo path in media folder
            profile.save()
            return redirect('profile')
        
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'current_profile': profile,
    }
    return render(request, 'profile.html', context)
def explore_view(request):
    # Filter posts based on the category
    category = request.GET.get('category', 'all')
    if category == 'all':
        posts = Post.objects.exclude(category='kids')
    else:
        posts = Post.objects.filter(category=category).exclude(category='kids')

    return render(request, 'explore.html', {'posts': posts})

from django.shortcuts import render
from .models import Post

def category_view(request, category_name):
    if category_name == 'friends':
        posts = Post.objects.filter(category='friends').exclude(author=request.user)
    elif category_name == 'kids':
        posts = Post.objects.filter(category='kids').exclude(author=request.user)
    elif category_name == 'mixed':
        posts = Post.objects.exclude(category='kids').exclude(author=request.user)
    else:
        posts = Post.objects.filter(category=category_name).exclude(author=request.user)
    
    context = {
        'posts': posts,
        'category_name': category_name
    }
    return render(request, 'category.html', context)


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Message

@login_required
def friends_list(request):
    friends = request.user.profile.friends.all()
    return render(request, 'friends_list.html', {'friends': friends})

@login_required
def chat_view(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend)) |
        (Q(sender=friend) & Q(receiver=request.user))
    ).order_by('timestamp')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=friend, content=content)
    return render(request, 'chat.html', {'friend': friend, 'messages': messages})




def explore(request):
    return render(request, 'explore.html')

def entertainment_category(request):
    # Implement logic to fetch and filter posts related to entertainment
    posts = Post.objects.filter(category='entertainment')  # Example query; adjust as per your models
    context = {
        'category_name': 'Entertainment',
        'posts': posts,
    }
    return render(request, 'category.html', context)

def education_category(request):
    # Implement logic to fetch and filter posts related to education
    posts = Post.objects.filter(category='education')  # Example query; adjust as per your models
    context = {
        'category_name': 'Education',
        'posts': posts,
    }
    return render(request, 'category.html', context)

def job_category(request):
    # Implement logic to fetch and filter posts related to jobs
    posts = Post.objects.filter(category='job')  # Example query; adjust as per your models
    context = {
        'category_name': 'Job',
        'posts': posts,
    }
    return render(request, 'category.html', context)

def news_category(request):
    # Implement logic to fetch and filter news posts
    posts = Post.objects.filter(category='news')  # Example query; adjust as per your models
    context = {
        'category_name': 'News or Updates',
        'posts': posts,
    }
    return render(request, 'category.html', context)

def shopping_category(request):
    # Implement logic to fetch and filter posts related to shopping
    posts = Post.objects.filter(category='shopping')  # Example query; adjust as per your models
    context = {
        'category_name': 'Shopping',
        'posts': posts,
    }
    return render(request, 'category.html', context)

def mixed_category(request):
    # Implement logic to fetch and filter posts related to mixed category
    posts = Post.objects.filter(category='mixed')  # Example query; adjust as per your models
    context = {
        'category_name': 'Mixed',
        'posts': posts,
    }
    return render(request, 'category.html', context)

# Add other category views as neededdef switch_mode(request, mode):
def switch_mode(request, mode):
    if mode == 'kids':
        request.session['mode'] = 'kids'
    else:
        request.session['mode'] = 'adult'
        # Optionally, you can set a default passcode here if not already set

    return redirect('kids_home')

def get_posts_based_on_mode(request):
    if request.session.get('mode') == 'kids':
        return Post.objects.filter(category='kids')  # Replace with your logic for kids posts
    else:
        return Post.objects.all()  # Regular mode shows all posts

def submit_passcode(request):
    if request.method == 'POST':
        passcode = request.POST.get('passcode')
        # Compare passcode with user-set passcode (stored in DB or session)
        if passcode == 'your_user_set_passcode':  # Replace with your actual passcode check
            request.session['mode'] = 'kids'  # Switch to kids mode after correct passcode
            return redirect('home')
        else:
            # Handle incorrect passcode scenario (e.g., show error message)
            pass  # Add your handling logic here

    return redirect('home')  
def kids_home_view(request):
     
     kids_posts = Post.objects.filter(category='kids')  # Adjust based on your category choice
     return render(request, 'kids_home.html', {'kids_posts': kids_posts})
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Post

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, FriendRequest, FriendSuggestion
from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, FriendRequest

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, FriendRequest

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, FriendRequest

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, FriendRequest
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, FriendRequest
@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    user_profile = Profile.objects.get(user=request.user)
    friends = request.user.profile.friends.all()
    friend_requests = FriendRequest.objects.filter(to_user=user)
    friend_ids = friends.values_list('user__id', flat=True)
    friend_suggestions = User.objects.exclude(id__in=friend_ids).exclude(id=request.user.id)

    # Get posts for friends and other categories
    friends_posts = Post.objects.filter(author__profile__in=friends).order_by('-created_at')
    category_posts = Post.objects.exclude(category='friends').order_by('-created_at')
    return render(request, 'home.html', {
        'user_profile': user_profile,
        'friend_requests': friend_requests,
        'friends': friends,
        'friends_posts': friends_posts,
        'category_posts': category_posts,
        'friend_suggestions': friend_suggestions
    })


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Message
from django.db.models import Q
@login_required
def view_friends(request):
    user = request.user
    friends = user.profile.friends.all()
    friends_profile = user.profile.profile_photo
    return render(request, 'chat_with.html', {
        'friends': friends, 'friends_profile': friends_profile
    })

@login_required
def chat_with(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    room_name = f'chat_{min(request.user.id, friend.id)}_{max(request.user.id, friend.id)}'
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend)) |
        (Q(sender=friend) & Q(receiver=request.user))
    ).order_by('timestamp')
    friends = get_friends(request.user)
    return render(request, 'chat_with.html', {
        'friend': friend,
        'room_name': room_name,
        'messages': messages,
        'friends': friends
    })
def get_friends(user):
    return UserFriendship.objects.filter(from_user=user).values_list('to_user', flat=True)

def view_friend_requests(request):
    received_requests = UserFriendship.objects.filter(to_user=request.user)
    sent_requests = UserFriendship.objects.filter(from_user=request.user)
    return render(request, 'home', {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    })
@login_required
def view_friend_suggestions(request):
    suggestions = User.objects.exclude(pk=request.user.pk).exclude(profile__friends=request.user)
    context = {
        'suggestions': suggestions,
    }
    return render(request, 'view_friend_suggestions.html', context)


from django.http import HttpResponseNotFound
@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=user)
    return redirect('home')

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    
    # Access the Profile instances of the users
    from_user_profile = friend_request.from_user.profile
    to_user_profile = friend_request.to_user.profile
    
    # Add friends to each other's profile
    to_user_profile.friends.add(from_user_profile)
    from_user_profile.friends.add(to_user_profile)
    
    # Delete the friend request after accepting it
    friend_request.delete()
    
    return redirect('home')

def ignore_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.delete()
    return redirect('home')
@login_required
def friends_category(request):
    posts = Post.objects.filter(category='friends')  # Filter posts for friends category
    context = {
        'category_name': 'Friends',
        'posts': posts,
    }
    return render(request, 'category.html', context)
@login_required
def kids_category(request):
    posts = Post.objects.filter(category='kids')  # Filter posts for kids category
    context = {
        'category_name': 'Kids',
        'posts': posts,
    }
    return render(request, 'category.html', context)
