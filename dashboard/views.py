# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import SignUpForm
from django.contrib.auth.views import password_reset as django_password_reset
from dashboard.forms import CustomPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    reset_password = False
    domain = request.META['HTTP_HOST']
    if ((domain+"/password_reset/") in str(HttpResponseRedirect(request.META.get('HTTP_REFERER'))).split("http://", 1)[1]):
        reset_password = True
    if request.user.is_authenticated:
        return redirect(reverse('search:index'))
    return render(request, 'dashboard/index.html', {'reset_password':reset_password})

def about(request):
    return render(request, 'dashboard/about.html')

def services(request):
    return render(request, 'dashboard/services.html')

def contact(request):
    return render(request, 'dashboard/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            domain = request.META['HTTP_HOST']
            confirmation_email(domain, form.cleaned_data.get('email'), user)
            return redirect(reverse('search:index'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def password_reset(*args, **kwargs):
    """
        Overriding the Email Password Resert Forms Save to be able to send HTML email
    """
    kwargs['password_reset_form'] = CustomPasswordResetForm
    return django_password_reset(*args, **kwargs)

def confirmation_email(domain, email, new_user):
    to = email
    token = default_token_generator.make_token(new_user)
    uid = urlsafe_base64_encode(force_bytes(new_user.pk))
    html_content = """<h3>Bem vindo %s </h3><p>Para confirmar seu registro no Novo Caminho clique no link abaixo:
    <a href='http://%s/confirmation/%s/%s'>Confirmação</a><br><p><b>Obrigado por se inscrever em nossos serviços.</b></p><br>
    <p>Aproveite!</p><small>Mensagem automática. Por favor no responda.</small>"""%(new_user.username, domain, uid, token)
    msg = EmailMultiAlternatives("Confirmação de email Novo Caminho", html_content, 'novocaminhocodenation@gmail.com', [to])
    msg.attach_alternative(html_content, 'text/html') #Definimos el contenido como html
    msg.send()

def activationview(request, uidb64, token):
    print (uidb64, token)
    if uidb64 is not None and token is not None:
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_text
        uid = urlsafe_base64_decode(uidb64)

        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        user = user_model.objects.get(pk=uid)

        if user is not None and default_token_generator.check_token(user, token):
            print("ENTROU NO IF")
            from django.contrib.auth.models import Group
            g = Group.objects.get(name='verified')
            g.user_set.add(user)
            return redirect('search:index')

    return redirect('login')
