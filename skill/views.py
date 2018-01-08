import os

from mimetypes import guess_type

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

# Create your views here.
from analytics.models import TagView
from dev.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin, 
			SubmitBtnMixin,
			AjaxRequiredMixin
			)

from artisan.models import ArtisanAccount
from artisan.mixins import ArtisanAccountMixin
from tag.models import Tag

from skill.forms import SkillAddForm, SkillModelForm
from skill.mixins import SkillManagerMixin
from skill.models import Skill, SkillRating, MySkills



class SkillRatingAjaxView(AjaxRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return JsonResponse({}, status=401)
		# credit card required ** 
		
		user = request.user
		skill_id = request.POST.get("Skill_id")
		rating_value = request.POST.get("rating_value")
		exists = Skill.objects.filter(id=skill_id).exists()
		if not exists:
			return JsonResponse({}, status=404)

		try:
			skill_obj = Skill.object.get(id=skill_id)
		except:
			skill_obj = Skill.objects.filter(id=skill_id).first()

		rating_obj, rating_obj_created = SkillRating.objects.get_or_create(
				user=user, 
				skill=skill_obj
				)
		try:
			rating_obj = SkillRating.objects.get(user=user, skill=skill_obj)
		except SkillRating.MultipleObjectsReturned:
			rating_obj = SkillRating.objects.filter(user=user, skill=skill_obj).first()
		except:
			#rating_obj = SkillRating.objects.create(user=user, Skill=Skill_obj)
			rating_obj = SkillRating()
			rating_obj.user = user
			rating_obj.skill = skill_obj
		rating_obj.rating = int(rating_value)
		myskills = user.myskills.skills.all()

		if skill_obj in mySkills:
			rating_obj.verified = True
		# verify ownership
		rating_obj.save()

		data = {
			"success": True
		}
		return JsonResponse(data)




class SkillCreateView(ArtisanAccountMixin, SubmitBtnMixin, CreateView):
	model = Skill
	template_name = "form.html"
	form_class = SkillModelForm
	#success_url = "/Skills/"
	submit_btn = "Add Skill"

	def form_valid(self, form):
		artisan = self.get_account()
		form.instance.artisan = artisan
		valid_data = super(SkillCreateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		if tags:
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.skill.add(form.instance)
		return valid_data


class SkillUpdateView(SkillManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Skill
	template_name = "form.html"
	form_class = SkillModelForm
	#success_url = "/Skills/"
	submit_btn = "Update Skill"

	def get_initial(self):
		initial = super(SkillUpdateView,self).get_initial()
		tags = self.get_object().tag_set.all()
		initial["tags"] = ", ".join([x.title for x in tags])
		"""
		tag_list = []
		for x in tags:
			tag_list.append(x.title)
		"""
		return initial

	def form_valid(self, form):
		valid_data = super(SkillUpdateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			tags_list = tags.split(",")
			
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.skills.add(self.get_object())
		return valid_data


	

class SkillDetailView(MultiSlugMixin, DetailView):
	model = Skill

	def get_context_data(self, *args, **kwargs):
		context = super(SkillDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		print (obj.artisan.mobile_number)
		tags = obj.tag_set.all()
		rating_avg = obj.skillrating_set.aggregate(Avg("rating"), Count("rating"))
		context["rating_avg"] = rating_avg
		if self.request.user.is_authenticated():
			rating_obj = SkillRating.objects.filter(user=self.request.user, skills=obj)
			if rating_obj.exists():
				context['my_rating'] = rating_obj.first().rating
			for tag in tags:
				new_view = TagView.objects.add_count(self.request.user, tag)
		return context


class SkillDownloadView(MultiSlugMixin, DetailView):
	model = Skill

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if not request.user.is_authenticated():
			raise Http404
		if obj in request.user.mySkills.Skills.all():
			filepath = os.path.join(settings.PROTECTED_ROOT, obj.image.path)
			guessed_type = guess_type(filepath)[0]
			wrapper = FileWrapper(file(filepath))
			mimetype = 'application/force-download'
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)
			
			if not request.GET.get("preview"):
				response["Content-Disposition"] = "attachment; filename=%s" %(obj.image.name)
			
			response["X-SendFile"] = str(obj.image.name)
			return response
		else:
			raise Http404



class ArtisanSkillListView(ArtisanAccountMixin, ListView):
	model = Skill
	template_name = "artisan/skill_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(ArtisanSkillListView, self).get_queryset(**kwargs)
		qs = qs.filter(artisan=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs




class VendorListView(ListView):
	model = Skill
	template_name = "skill/skill_list.html"

	def get_object(self):
		username= self.kwargs.get("vendor_name")
		artisan = get_object_or_404(ArtisanAccount, user__username=username)
		return artisan

	def get_context_data(self, *args, **kwargs):
		context = super(VendorListView, self).get_context_data(*args, **kwargs)
		context["vendor_name"] = str(self.get_object().user.username)
		return context

	def get_queryset(self, *args, **kwargs):
		artisan = self.get_object()
		qs = super(VendorListView, self).get_queryset(**kwargs).filter(artisan=artisan)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs

	

class SkillListView(ListView):
	model = Skill

	def get_queryset(self, *args, **kwargs):
		qs = super(SkillListView, self).get_queryset(**kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs


class UserLibraryListView(LoginRequiredMixin, ListView):
	model = MySkills
	template_name = "skills/library_list.html"

	def get_queryset(self, *args, **kwargs):
		obj = MySkills.objects.get_or_create(user=self.request.user)[0]
		qs = obj.skills.all()
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs
























def create_view(request): 
	form = SkillModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
			"form": form,
			"submit_btn": "Create Skill"
		}
	return render(request, template, context)


def update_view(request, object_id=None):
	skill = get_object_or_404(Skill, id=object_id)
	form = SkillModelForm(request.POST or None, instance=Skill)
	if form.is_valid():
		instance = form.save(commit=False)
		#instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
		"object": skill,
		"form": form,
		"submit_btn": "Update Skill"
		}
	return render(request, template, context)



def detail_slug_view(request, slug=None):
	skill = Skill.objects.get(slug=slug)
	try:
		skill = get_object_or_404(Skill, slug=slug)
	except Skill.MultipleObjectsReturned:
		skill = Skill.objects.filter(slug=slug).order_by("-title").first()
	# print slug
	# Skill = 1
	template = "detail_view.html"
	context = {
		"object": skill
		}
	return render(request, template, context)


def detail_view(request, object_id=None):
	skill = get_object_or_404(Skill, id=object_id)
	template = "detail_view.html"
	context = {
		"object": skill
		}
	return render(request, template, context)

	# if object_id is not None:
	# 	Skill = get_object_or_404(Skill, id=object_id)
	# 	# Skill = Skill.objects.get(id=object_id)
	# 	# try:
	# 	# 	Skill = Skill.objects.get(id=object_id)
	# 	# except Skill.DoesNotExist:
	# 	# 	Skill = None

		
	# else:
	# 	raise Http404


def list_view(request):
	# list of items
	queryset = Skill.objects.all()
	template = "list_view.html"
	context = {
		"queryset": queryset
	}
	return render(request, template, context)




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