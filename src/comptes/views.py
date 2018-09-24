# -*- coding: utf-8 -*-
from django.contrib.auth            import authenticate, login, get_user_model
from django.contrib.auth.models     import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib                 import messages
from django.core.urlresolvers       import reverse
from django.utils.decorators        import method_decorator
from django.views.generic           import CreateView, FormView, DetailView, ListView, View, UpdateView
from django.views.generic.edit      import FormMixin
from django.http                    import HttpResponse, HttpResponseRedirect
from django.shortcuts               import render,redirect

from django.utils.http              import is_safe_url
from django.utils.safestring        import mark_safe
from rolepermissions.roles          import assign_role

from sbeeapp.mixins     import NextUrlMixin, RequestFormAttachMixin
from .forms             import LoginForm, RegisterForm, ReactivateEmailForm, UserDetailChangeForm
from .models            import User, EmailActivation
from .signals           import user_logged_in
from factures.models    import Facture

# def group_perm(request):
#     # creating the group
#     new_group, created = Group.objects.get_or_create(name ='Abonne')
#     # Code to add permission to group
#     ct = ContentType.objects.get_for_model(User)
     
#     # If I want to add 'Can go Haridwar' permission to level0 ?
#     ('VIEW_FILES', 'can view files and related stuff')
#     permission = Permission.objects.create(codename ='VIEW_FILES', name='Can view files and related stuff', content_type=ct)
#     new_group.permissions.add(permission)

#     new_group.user_set.add(request.user)




class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'comptes/details.html'

    def get_queryset(self, *args, **kwargs):
        impaye = Facture.objects.get(ref__exact=self.request.user.ref_abonne)
        context = { 'user' : self.request.user , 'impaye' : impaye}

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        impaye = Facture.objects.filter(ref__exact=self.request.user.ref_abonne)
        context = { 'user' : self.request.user , 'impaye' : impaye}
        print(context)
        return context




class UserListView(LoginRequiredMixin, ListView):
    queryset = User.objects.all()
    template_name = "comptes/list.html"



class UsersDetailView(LoginRequiredMixin, DetailView):
    queryset = User.objects.all()
    template_name = 'comptes/details.html'



class UserEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Votre compte a été activé. Vous pouvez desormais vous connecter")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Votre compte a deja été activé. <a href="{link}">restaurer votre mot de passse</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login") 
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        request = self.request
        messages.success(request, "Email d'Activation envoyé. Verifiez votre boite mail afin de proceder à l'activation de votre compte.")
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        assign_role(user, 'abonne')
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(UserEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)



class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/factures'
    template_name = 'auth/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/login'



class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'comptes/update.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Changer les details de votre compte'
        return context

    def get_success_url(self):
        return reverse("compte:user_detail")

    
def disable_enable_user(request, pk):
    user = User.objects.get(pk = pk)
    if user.is_active :
        user.is_active = False
        messages.success(request, 'Compte de l\'utilisateur désactivé')
    else:
        user.is_active = True
        messages.success(request, 'Compte de l\'utilisateur activé')
    user.save()
    return redirect('compte:user_detail')