from django import forms
from .models import UserInfo


class LoginForm(forms.ModelForm):
    login_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'please enter user name'}))
    login_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please enter your password'}))

    class Meta:
        model = UserInfo
        fields = ('login_username', 'login_password')

class UserRegistrationForm(forms.ModelForm):

    sign_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'please enter user name'}))
    sign_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please enter your password'}))
    sign_confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please enter your password again'}))
    sign_email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Please input the email address'}))

    class Meta:
        model = UserInfo
        fields = ('sign_username', 'sign_password', 'sign_confirm_password', 'sign_email')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return confirm_password