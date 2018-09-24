from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		user = request.user
		created = False
		billing_profile = None
		if user.is_authenticated:
			billing_profile, billing_profile_created = self.model.objects.get_or_create(email=user.email)
		# elif guest_email_id is not None:
		# 	guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
		# 	billing_profile, billing_guest_profile_created = self.model.objects.get_or_create(email=guest_email_obj.email)
		else:
			pass

		return billing_profile, created



class BillingProfile(models.Model):
	"""docstring for BillingProfile"""
	user 		= models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	email 		= models.EmailField()
	active 		= models.BooleanField(default=True)
	update 		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)

	objects = BillingProfileManager()

	def __str__(self):
		return self.email


# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		print('Send to stripe')
# 		instance.customer_id = newID
# 		instance.save()

def user_created_receiver(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)