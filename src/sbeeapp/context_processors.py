from factures.models import Facture

def factures_count(request):
	count = Facture.objects.count()
	return {'count' : count}
