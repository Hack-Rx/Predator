from django import forms

class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()

class CalorieForm(forms.Form):
    image = forms.ImageField()