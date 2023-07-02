from django import forms
from .models import User_Profile, AndroidApp,Screenshot
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name', 'phone_number', 'email',)

class AndroidAppForm(forms.ModelForm):
    class Meta:
        model = AndroidApp
        fields = '__all__'

class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = Screenshot
        fields = ['screenshot',]



"""class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User_Profile
        fields = ('name', 'points_earned', 'tasks_completed', 'password')"""


