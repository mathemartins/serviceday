from django.contrib import admin

# Register your models here.
from sellers.models import SellerAccount

class SellersModelAdmin(admin.ModelAdmin):
	list_display = ["__str__", "active", "timestamp"]
	search_fields = ["__str__", "managers"]
	list_filter = ["active", "managers", "timestamp"]
	list_editable = ["active"]
	
	class Meta:
		model = SellerAccount

admin.site.register(SellerAccount, SellersModelAdmin)