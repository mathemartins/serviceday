from django.conf.urls import include, url
from django.contrib import admin

from artisan.views import (
        	ArtisanDashboard,
        	ArtisanSkillDetailRedirectView,
        )

from skill.views import (
		SkillCreateView,
		SkillUpdateView,
		ArtisanSkillListView,
	)


urlpatterns = [
    url(r'^$', ArtisanDashboard.as_view(), name='dashboard'),
    url(r'^skill/$', ArtisanSkillListView.as_view(), name='artisan_list'), #sellers:product_list
    url(r'^skill/(?P<pk>\d+)/$', ArtisanSkillDetailRedirectView.as_view()),
    url(r'^skill/(?P<pk>\d+)/edit/$', SkillUpdateView.as_view(), name='artisan_edit'),
    url(r'^skill/add/$', SkillCreateView.as_view(), name='artisan_create'),
]  