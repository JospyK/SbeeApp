# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm
from factures.models import Facture
from django.contrib.auth.decorators import login_required

def home_page(request):
    context = {"title": "hello"}
    return render(request, "home_page.html", context)


@login_required()
def dash_page(request):
    all_factures_count1 = Facture.objects.all().count() # vos factures impayés
    all_factures_count2 = Facture.objects.all()         # votre nombre de facture exact
    all_factures_count3 = Facture.objects.all().count() # nombre de facture total de tous les users (admin)
    all_factures_count4 = Facture.objects.all().count() # le nombre total d'utilisateurs
    context = {
        "a1": all_factures_count1,
        "a2": all_factures_count2,
        "a3": all_factures_count3,
        "a4": all_factures_count4,
    }
    return render(request, "dash_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'role': 'role1',
        'form': contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, "contact/index.html", context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {'form' : form}
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated())
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)
            #context['form'] = LoginForm()
            return redirect("/admin")
        else:
            print("Error")

    return render(request, "auth/login.html", context)
    
# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {'form' : form}
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         new_user = User.objects.create_user(username, email, password)
#         print(user)
#     return render(request, "auth/register.html", context)