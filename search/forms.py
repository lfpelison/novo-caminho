# -*- coding: utf-8 -*-
from django import forms


class SearchForm(forms.Form):
    ENGINES = (
        ('google', 'Google'),
        ('yahoo', 'Yahoo'),
        ('bing', 'Bing'),
    )
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'style':'font-size:15px', 'size': 35, 'placeholder': 'Digite sua busca, separada por vírgulas.'}))
    engines = forms.MultipleChoiceField(label="Selecione pelo menos 1", choices=ENGINES,
            required=True, error_messages={'required': 'Por favor, preenche pelo menos uma fonte de buscas'},
            widget=forms.CheckboxSelectMultiple(), initial=('google',))
