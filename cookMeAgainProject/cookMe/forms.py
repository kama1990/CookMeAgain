from django import forms
from .models import Recipe

class EmailPostForm(forms.Form):
    name = forms.CharField(label='Użytkownik',max_length=40)
    email = forms.EmailField(label='Twój email') # owener email
    to = forms.EmailField(label='Email odbiorcy') # person email who will receive email
    comments = forms.CharField(label='Wiadomość',
                               required=False,
                               widget=forms.Textarea)
    

class RecipePostForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('create_date', 'user')
