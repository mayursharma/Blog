from django import forms

from django.contrib.auth.models import User
from models import *


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('added','user',)
        widgets ={'picture' : forms.FileInput()}
        