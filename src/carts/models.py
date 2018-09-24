from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from factures.models import Facture

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
	def new_or_get(self, request):
		cart_id = request.session.get('cart_id', None)
		qs = self.get_queryset().filter(id=cart_id)
		if qs.count() == 1:
			new_obj = False
			cart_obj = qs.first()
			if request.user.is_authenticated and cart_obj.user is None:
				cart_obj.user = request.user
				cart_obj.save()
		else:
			cart_obj = self.new(user=request.user)
			new_obj = True
			request.session['cart_id'] = cart_obj.id
		return cart_obj, new_obj

	def new(self, user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)

		
class Cart(models.Model):
	"""docstring for Cart"""
	user 		= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	factures	= models.ManyToManyField(Facture, blank=True)#create empty cart
	total		= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	timestamp	= models.DateTimeField(auto_now_add=True)
	update		= models.DateTimeField(auto_now=True)
	objects 	= CartManager()

	def __str__(self):
		return str(self.id)


def pre_save_cart_receiver(sender, instance, action, *args, **kwargs):
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
		factures = instance.factures.all()
		total = 0
		for x in factures:
			total += x.net_a_payer
		instance.total = total
		instance.save()

m2m_changed.connect(pre_save_cart_receiver, sender=Cart.factures.through)