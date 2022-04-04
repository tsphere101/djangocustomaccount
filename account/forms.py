from cProfile import label
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate

from account.models import Account

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ('email','password',)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError(
                    'Either your login email or password is incorrect.')

class RegistrationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    email = forms.EmailField(
        max_length=255, help_text="Required. Add a valid email address."
    )

    class Meta:
        model = Account
        fields = ("email", 'first_name','last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data[
            "email"
        ].lower()  # 'email' has to be matched in the html input name='email'

        # Check if account already exist
        try:
            account = Account.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(f"Account with email {email} is already existed.")
