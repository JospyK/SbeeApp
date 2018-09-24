# -*- coding: utf-8 -*-
from django                     import forms
from django.contrib.auth        import authenticate, login, get_user_model
from django.contrib.auth.forms  import ReadOnlyPasswordHashField
from django.core.urlresolvers   import reverse
from django.utils.safestring    import mark_safe
from rolepermissions.roles      import assign_role

User = get_user_model()

from .models import EmailActivation


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your email"}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email) 
        if not qs.exists():
            register_link = reverse("register")
            msg = """Cette adresse email n'est pas enrégistrée, voulez vous <a href="{link}">créer un compte</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('nom', 'prenoms', 'email', 'ref_abonne')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            assign_role(user, 'abonne')
            assign_role(user, 'admin')
        return user



class UserDetailChangeForm(forms.ModelForm):
    # full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    class Meta:
        model = User
        fields = ('nom', 'prenoms', 'telephone')
        widgets = {
            'nom':          forms.TextInput(attrs={'placeholder': 'Nom',        'class': 'input100'}),
            'prenoms':      forms.TextInput(attrs={'placeholder': 'Prenoms',    'class': 'input100'}),
            'telephone':    forms.TextInput(attrs={'placeholder': 'Telephone',    'class': 'input100'}),
        }


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('nom', 'prenoms', 'ref_abonne', 'email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": "input100", "placeholder": "Email"}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Mot de passe"}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email  = data.get("email")
        password  = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ## not active, check email activation
                link = reverse("compte:resend-activation")
                reconfirm_msg = """<a href='{resend_link}'>
                Renvoyer l'email de confirmation</a>.
                """.format(resend_link = link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Vérifier votre boite email pour activer votre compte ou " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Adresse email non confirmée. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("Ce compte est inactif.")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Informations de connexion incorrects")
        login(request, user)
        self.user = user
        return data

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        
        print(user)
        if user is not None:
            if not user.is_active:
                print('inactive user..')
                messages.success(request, "This user is inactive")
                return super(LoginView, self).form_invalid(form)
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Mot de passe"}))
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Confirmation mot de passe"}))

    class Meta:
        model = User
        fields = ('nom', 'prenoms', 'ref_abonne', 'email',)
        widgets = {
            'nom':          forms.TextInput(attrs={'placeholder': 'Nom',        'class': 'input100'}),
            'prenoms':      forms.TextInput(attrs={'placeholder': 'Prenoms',    'class': 'input100'}),
            'email':        forms.TextInput(attrs={'placeholder': 'Email',      'class': 'input100'}),
            'ref_abonne':   forms.TextInput(attrs={'placeholder': 'Reference Abonne', 'class': 'input100'}),
        }


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False # send confirmation email via signals
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            user.save()
        return user