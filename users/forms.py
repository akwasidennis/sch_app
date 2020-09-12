from django import forms
from .models import UserProfile, COURSE_CHOICES
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
# from assignment.models import SELECT_COURSE
User = get_user_model()

STATUS = (
            ('graded', 'graded'),
             ('not graded', 'graded'),
    )
class UserRegisterForm(UserCreationForm):
    
    # course = forms.ChoiceField(choices=SELECT_COURSE)
    email = forms.EmailField(max_length=150)
    index_number = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('index_number', 'email', 'password1', 'password2',)
      

    def clean_index_number(self, *args, **kwargs):
        index = self.cleaned_data.get('index_number')
        qs = User.objects.filter(index_number=index)
        if qs.exists():
            raise forms.ValidationError("This index number has already been used!")
        return index


    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.index_number = self.cleaned_data['index_number']

        if commit:
            user.save()
            print('Its saved')
        return user
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=150)
    index_number = forms.CharField(max_length=150)
    # course = forms.CharField(widget=forms.Select(choices=COURSE_CHOICES), max_length=100)

    class Meta:
        model = User
        fields = ('index_number', 'email',)
        


class UserProfileUpdateForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ['image']



# class CustomAuthenticationForm(AuthenticationForm):
#     index_number = UsernameField(
#         label='Index number',
#         widget=forms.TextInput(attrs={'autofocus': True})
#     )
