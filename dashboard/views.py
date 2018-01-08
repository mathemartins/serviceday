import random

from django.views.generic import View
from django.shortcuts import render

# Create your views here.

from skill.models import Skill, CuratedSkills
from core.models import BannerContentControl

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		tag_views = None
		skill = None
		top_tags = None
		curated = CuratedSkills.objects.filter(active=True).order_by("?")
		text = BannerContentControl.objects.all
		try:
			tag_views = request.user.tagview_set.all().order_by("-count")[:5]
		except:
			pass

		owned = None

		try:
			owned = request.user.myskills.skills.all()
		except:
			pass

		if tag_views:
			top_tags = [x.tag for x in tag_views]
			skill = Skill.objects.filter(tag__in=top_tags)
			if owned:
				skill = skill.exclude(pk__in=owned)

			if skill.count() < 10:
				skill = Skill.objects.all().order_by("?")
				if owned:
					skill = skill.exclude(pk__in=owned)
				skill = skill[:4]
			else:
				skill = skill.distinct()
				skill = sorted(skill, key= lambda x: random.random())

		context = {
			"skill": skill,
			"top_tags": top_tags,
			"curated": curated,
			"text":text
		}
		return render(request, "dashboard/view.html", context)

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