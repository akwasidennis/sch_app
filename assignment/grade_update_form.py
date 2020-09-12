from django import forms

from .models import Profile, StudentResult
from .utils import Utils


class StudentResultForm(forms.ModelForm):
    class Meta:
        model = StudentResult
        fields = ('title', 'status', 'scored', 'total', 'marker', 'date_graded',)
 