from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']




from django import forms
from .models import Profile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    delete_profile_photo = forms.BooleanField(required=False, initial=False, label='Delete Profile Photo')
    
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio', 'delete_profile_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),  # Set the number of rows to 3
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

# forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','link', 'image', 'video', 'media_tag', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Invalid login. Please ensure your username and password are correct."
        ),
        'inactive': "This account is inactive.",
    }
