from django import forms
from .models import Profile, Food, Walk

class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()

class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['food_image']

class WalkForm(forms.ModelForm):

    class Meta:
        model = Walk
        fields = ['steps']

class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'height', 'weight', 'gender', 'workout']

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name','weight']