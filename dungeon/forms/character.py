from django import forms


class CharacterForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    image_url = forms.CharField(label='Icon', max_length=500)