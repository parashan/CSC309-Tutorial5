from django import forms
from django.core.exceptions import ValidationError
from .models import Chat

def length_check(length):
    def check_length(value):
        if len(value) < length:
            raise ValidationError(('This field needs to be %(length)s characters long'), params={'length': length}, code='invalid')
    return check_length
    
class EnterForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), validators = [])

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), validators = [])

class RegisterForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), validators = [])
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), validators = [])
    birth_date = forms.DateField(label="Birth Date", widget=DateInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    
    def clean(self):
        super().clean()
        password = self.cleaned_data['password1']
        password_c = self.cleaned_data['password2']
        if password != password_c:
            # Throw an error 
            raise ValidationError("The two password fields didn't match")
            # OR call self.add_error
            # self.add_error(None, "The two password fields didn't match")

class ChatForm(forms.Form):
    comment=forms.CharField(widget=forms.Textarea, max_length=1000)

class ChatModelForm(forms.ModelForm):
    class Meta:
        model=Chat
        fields=["comment"]
        widgets={"comment": forms.Textarea}

   