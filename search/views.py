from django.shortcuts import render

# Create your views here.
from products.models import Product
from sellers.models import Artisan

def search_view(request):
	qs_prod = Product.objects.all()
	qs_artisan = Artisan.objects.all()

	query = self.request.GET.get("q")
	if query:
		qs_artisan = qs.filter(
			Q(title__icontains=query)|
			Q(description__icontains=query)
		).order_by("title")
	return qs_artisan