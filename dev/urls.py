"""dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from dashboard.views import DashboardView
from skill.views import UserLibraryListView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^artisan/', include("artisan.urls", namespace='artisan')),
    url(r'^skill/', include("skill.urls", namespace='skill')),
    url(r'^tags/', include("tag.urls", namespace='tag')),
    url(r'^category/', include("core.urls", namespace='cat')),
    url(r'^library/', UserLibraryListView.as_view(), name='library'),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
