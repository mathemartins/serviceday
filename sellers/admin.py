from django.contrib import admin

# Register your models here.
from sellers.models import SellerAccount, ArtisanAccount

class SellerAccountAdmin(admin.ModelAdmin):
	list_display = ["__str__", "active", "timestamp"]
	search_fields = ["__str__", "managers"]
	list_filter = ["active", "managers", "timestamp"]
	list_editable = ["active"]
	
	class Meta:
		model = SellerAccount

admin.site.register(SellerAccount, SellerAccountAdmin)

class ArtisanAccountAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active', 'timestamp', 'job_title')
    list_filter = ('active', 'timestamp', 'job_title')
    list_editable = ('active',)
    search_fields = ('__str__', 'job_title',)

    class Meta:
    	model = ArtisanAccount

admin.site.register(ArtisanAccount, ArtisanAccountAdmin)
