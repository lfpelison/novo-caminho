from django import forms

class SearchForm(forms.Form):
    ENGINES = (
        ('google', 'Google'),
        ('yahoo', 'Yahoo'),
        ('bing', 'Bing'),
    )
    query = forms.CharField(label='Query', max_length=100)
    engines = forms.MultipleChoiceField(choices=ENGINES, widget=forms.CheckboxSelectMultiple())
