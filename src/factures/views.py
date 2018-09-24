from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from .models import Facture

from django.template import RequestContext

class FactureListView(LoginRequiredMixin, ListView):
	#queryset = Facture.objects.filter(user_ref__iexact=self.request.user.ref_abonne)
	template_name = "factures/list.html"

	def get_queryset(self, *args, **kwargs):
		request = Facture.objects.filter(ref__exact=self.request.user.ref_abonne)
		return request


class FactureDetailView(LoginRequiredMixin, DetailView):
	queryset = Facture.objects.all()
	template_name = "factures/details.html"

	def get_context_data(self, *arg, **kwargs):
		context = super(FactureDetailView, self).get_context_data(*arg, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context["cart"] = cart_obj
		return context


class UserFactureHistoryView(LoginRequiredMixin, ListView):
	template_name = "factures/user-history.html"
	def get_context_data(self, *args, **kwargs):
		context = super(UserFactureHistoryView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Facture, model_queryset=False)
		return views

