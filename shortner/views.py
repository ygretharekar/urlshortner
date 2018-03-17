import random, string
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
# Create your views here.

from .models import URLShortner


def index(request):
	return render(request, 'index.html')


def get_hash():
	c = string.ascii_uppercase + string.digits + string.ascii_lowercase

	return ''.join(random.choice(c) for x in range(8))

from django.http import JsonResponse
from .forms import ShortenURLForm, CountForm, LongForShortForm

def shorten_url(request):

	if request.method == 'POST':

		url = ShortenURLForm(request.POST)

		if url.is_valid():

			short_id = get_hash()

			short_url = settings.SITE_URL + '/' + short_id	

			# data = ShortenURLForm(url=url, short_id=short_id)  # pylint: disable=E1123
			URLShortner.objects.create(url=url.cleaned_data['long_url'], short_id=short_id)  # pylint: disable=E1101

			# data.save()  # pylint: disable=E1101

			return JsonResponse({
				"short_url": short_url,
				"status": "OK",
				"status_codes": []
			})

		else:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["INVALID_URLS"]
			})

	else:
		url = ShortenURLForm(initial={'long_url': 'https://www.hackerearth.com'})

	return render(
		request,
		'shortner/shorten_url.html',
		{'form':url}
	)



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def clean_urls(request):
	URLShortner.objects.all().delete()  # pylint: disable=E1101
	return redirect('index')

class ShortenURL(CreateView):
	model= URLShortner
	fields = ['url']
	initial = {'url': 'https://www.hackerearth.com'}



def redirect_long_from_short(request, pk):
	url = get_object_or_404(URLShortner, pk=pk)
	url.count += 1
	url.save()
	return redirect(url.url)



def count_redirects(request):
	if request.method == 'POST':

		slug = CountForm(request.POST)

		if slug.is_valid():

			d = slug.cleaned_data['short_url'].split('/')[-1]

			count = get_object_or_404(URLShortner, pk=d)

			c = count.count

			return JsonResponse({
				"count": c,
				"status": "OK",
				"status_codes": []
			})

		else:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["SHORT_URL_NOT_FOUND"]
			})

	else:
		count = CountForm()

	return render(
		request,
		'shortner/count_form.html',
		{'form': count}
	)


def fetch_long_for_short(request):
	if request.method == 'POST':

		slug = LongForShortForm(request.POST)

		if slug.is_valid():

			d = slug.cleaned_data['short_url'].split('/')[-1]

			count = get_object_or_404(URLShortner, pk=d)

			c = count.url

			return JsonResponse({
				"long_url": c,
				"status": "OK",
				"status_codes": []
			})

		else:
			return JsonResponse({
				"status": "FAILED",
				"status_codes": ["SHORT_URL_NOT_FOUND"]
			})

	else:
		count = LongForShortForm()

	return render(
		request,
		'shortner/long_for_short.html',
		{'form': count}
	)

