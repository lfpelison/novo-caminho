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
from django.contrib.auth.tokens import default_token_generator

class CustomPasswordResetForm(PasswordResetForm):
    """
        Overriding the Email Password Resert Forms Save to be able to send HTML email
    """
    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, request=None, email_subject_name='registration/password_reset_subject.txt', **kwargs):
        from django.core.mail import EmailMultiAlternatives
        from django.utils.html import strip_tags
        from django.template.loader import render_to_string
        from django.contrib.sites.models import get_current_site
        from django.utils.http import int_to_base36

        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                 site_name = domain = domain_override

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            render = render_to_string(email_template_name, c)
            render_subject = render_to_string(email_subject_name, c)

            msg = EmailMultiAlternatives(render_subject, strip_tags(render), None, [user.email])
            msg.attach_alternative(render, "text/html")
            msg.send()
