from django.contrib.auth.decorators import login_required
from django.shortcuts 	import render, redirect
from billing.models 	import BillingProfile
from comptes.forms 		import LoginForm
from orders.models 		import Order
from factures.models 	import Facture
from .models 			import Cart



@login_required()
def home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render(request, "cart/index.html", {"cart": cart_obj})


@login_required()
def update(request):
	facture_id = request.POST.get('facture_id')
	if facture_id is not None:
		try:
			facture_obj = Facture.objects.get(id=facture_id)
		except Facture.DoesNotExist:
			print("Show message to user product is gone")
			return redirect("carts:index")

		cart_obj, new_obj = Cart.objects.new_or_get(request)

		if facture_obj in cart_obj.factures.all():
			cart_obj.factures.remove(facture_obj)
		else:
			cart_obj.factures.add(facture_obj)

		request.session['cart_items_count'] = cart_obj.factures.count()
		print(request.session['cart_items_count'])
	return redirect("carts:index")


@login_required()
def checkout(request):
	print("ok")
# 	cart_obj, cart_created = Cart.objects.new_or_get(request)
# 	order_obj = None
# 	if cart_created or cart_obj.factures.count() == 0:
# 		return redirect("cart:home")

# 	login_form = LoginForm()
# #	billing_profile, billing_guest_profile_created = BillingProfile.objects.new_or_get(request)

# 	if billing_profile is not None:
# 		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		

# 	context = {
# 		"order": order_obj,
# 		"billing_profile": billing_profile,
# 		"login_form": login_form,
# 	}
# 	return render(request, 'cart/checkout.html', context)
	return htt