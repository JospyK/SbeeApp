from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()     


class ContactForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Your content"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError('Email has to be gmail')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your email"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Your name"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your email"}))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your content"}))
    #numero = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your password"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Your password"}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Your password"}))

    def username_already_exist(self):
        username = self.cleaned_data.get('username')
        qs = User.object.filter(username=username)
        if qs.exist():
            raise forms.ValidationError('Un compte utilise deja ce numero de telephone')

    def email_already_exist(self):
        email = self.cleaned_data.get('email')
        qs = User.object.filter(email=email)
        if qs.exist():
            raise forms.ValidationError('Un compte utilise deja ce numero de telephone')

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError('Les mots de passes doivent etre identiques')
        return data
