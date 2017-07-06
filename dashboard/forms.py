from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=False,
            widget=forms.TextInput(attrs={'maxlength':5, 'placeholder': 'Primeiro nome'}))
    last_name = forms.CharField(max_length=20, required=False,
            widget=forms.TextInput(attrs={'maxlength':5, 'placeholder': 'Segundo nome'}))
    email = forms.EmailField(max_length=254,
            widget=forms.TextInput(attrs={'maxlength':5, 'placeholder': 'E-mail'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

#widget=forms.TextInput(
#    attrs={'size': 5, 'class': 'form-control', 'placeholder': 'First Name'})
