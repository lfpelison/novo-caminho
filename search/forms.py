# -*- coding: utf-8 -*-
from django import forms
from search.models import Keyword

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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['keywords'] = forms.MultipleChoiceField(required=False,
            choices=[ (o.name, str(o.name)) for o in Keyword.objects.filter(user=user)],
            widget=forms.CheckboxSelectMultiple(),
            )
