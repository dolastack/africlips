from django import forms
from .models import YoutubeFeed


class YoutubeFeedForm(forms.ModelForm):
    class Meta:
        model = YoutubeFeed
        fields = ('url', 'external_id')
