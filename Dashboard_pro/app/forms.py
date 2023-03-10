from django import forms
from .models import upload

class uploadform(forms.ModelForm):
    class Meta:
        model = upload
        fields = ('file',)