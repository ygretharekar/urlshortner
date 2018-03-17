from django import forms


class ShortenURLForm(forms.Form):
	long_url = forms.URLField(help_text='Enter url to be shortened')
	def clean_long_url(self):
		data = self.cleaned_data['long_url']
		return data


class CountForm(forms.Form):
	short_url = forms.URLField(help_text='Find number of redirects')
	def clean_count(self):
		data = self.cleaned_data['short_url']
		return data

class LongForShortForm(forms.Form):
	short_url = forms.URLField(help_text='Get long url for short url')
	def clean_count(self):
		data = self.cleaned_data['short_url']
		return data



