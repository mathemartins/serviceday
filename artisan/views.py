from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404



from artisan.forms import NewArtisanForm
from artisan.mixins import ArtisanAccountMixin
from artisan.models import ArtisanAccount


class ArtisanSkillDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()



class ArtisanDashboard(ArtisanAccountMixin, FormMixin, View):
	form_class = NewArtisanForm
	success_url = '/artisan/'

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get(self, request, *args, **kwargs):
		apply_form = self.get_form() #NewSellerForm()
		account = self.get_account()
		exists = account
		active = None
		context = {}
		if exists:
			active = account.active
		if not exists and not active:
			context["title"] = "Apply for Account"
			context["apply_form"] = apply_form
		elif exists and not active:
			context["title"] = "Account Activation Pending"
		elif exists and active:
			context["title"] = "Artisan Dashboard"
			
			#products = Product.objects.filter(seller=account)
			context["skills"] = self.get_skills()
			# transactions_today = self.get_transactions_today()
			# context["transactions_today"] = transactions_today
			# context["today_sales"] = self.get_today_sales()
			# context["total_sales"] = self.get_total_sales()
			# context["transactions"] = self.get_transactions().exclude(pk__in=transactions_today)[:5]
		else:
			pass
		
		return render(request, "artisan/dashboard.html", context)

	def form_valid(self, form):
		valid_data = super(ArtisanDashboard, self).form_valid(form)
		obj = ArtisanAccount.objects.create(user=self.request.user)
		return valid_data


from django.shortcuts import render

# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from analytics.models import TagView
from tag.models import Tag


class TagDetailView(DetailView):
	model = Tag


	def get_context_data(self, *args, **kwargs):
		context = super(TagDetailView, self).get_context_data(*args, **kwargs)
		if self.request.user.is_authenticated():
			tag = self.get_object()
			new_view = TagView.objects.add_count(self.request.user, tag)
		return context



class TagListView(ListView):
	model = Tag

	def get_queryset(self):
		return Tag.objects.all()