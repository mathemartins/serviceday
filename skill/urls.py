from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from skill.views import (
        SkillCreateView,
        SkillDetailView,
        SkillDownloadView,
        SkillListView, 
        SkillUpdateView,
        SkillRatingAjaxView,
        VendorListView,
        )

urlpatterns = [
    url(r'^$', SkillListView.as_view(), name='list'), #Skills:list
    url(r'^vendor/$', RedirectView.as_view(pattern_name='skills:list'), name='vendor_list'),
    url(r'^vendor/(?P<vendor_name>[\w.@+-]+)/$', VendorListView.as_view(), name='vendor_detail'),
    url(r'^ajax/rating/$', SkillRatingAjaxView.as_view(), name='ajax_rating'),
    url(r'^(?P<pk>\d+)/$', SkillDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', SkillDetailView.as_view(), name='detail_slug'),
    url(r'^(?P<pk>\d+)/download/$', SkillDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', SkillDownloadView.as_view(), name='download_slug'),
    url(r'^(?P<pk>\d+)/edit/$', SkillUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', SkillUpdateView.as_view(), name='update_slug'),
   

]   
