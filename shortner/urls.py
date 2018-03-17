from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('fetch/short-url/', views.shorten_url, name='shorten_url'),
	path('fetch/long-url/', views.fetch_long_for_short, name='long_for_short'),
	path('fetch/count/', views.count_redirects, name='count_redirects'),
	path('<slug:pk>/', views.redirect_long_from_short, name='redirect_long'),
	path('clean-urls/', views.clean_urls, name='clean_urls'),
]
