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

from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader

class CustomPasswordResetForm(PasswordResetForm):
    """
        Overriding the Email Password Resert Forms Save to be able to send HTML email
    """
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
            Sends a django.core.mail.EmailMultiAlternatives to 'to_email'.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        # New line introduce
        email_message.attach_alternative(body, 'text/html')

        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
