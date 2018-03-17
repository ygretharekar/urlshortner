from django.test import TestCase






# Create your tests here.
import json
import httplib2 as httplib
import requests
import sys
import unittest

from .constants import (FETCH_SHORT_URL_ENDPOINT, FETCH_LONG_URL_ENDPOINT,
                       FETCH_SHORT_URLS_ENDPOINT, FETCH_LONG_URLS_ENDPOINT,
                       FETCH_COUNT_ENDPOINT, CLEAN_URL_ENDPOINT)


class TestURLShortener(unittest.TestCase):

	url = "http://localhost:8000/"

	def setUp(self):

		# Clean the database
		self.post(CLEAN_URL_ENDPOINT)

	def post(self, end_point, data=None, construct_url=True):
		"""
		Make a post request
		"""
		if data is None:
			data = {}

		url = end_point
		if construct_url:
			url = self.url + end_point

		headers = {
			'Content-type': 'application/json'
		}

		response = requests.post(url, data=json.dumps(data), headers=headers)

		return response


	def checkResponseOK(self, response):
		"""
		Check if response returned 200 OK
		"""
		self.assertEqual(response.status_code, 200,
		                 "Server did not return 200 OK!!!")

	def getResponseContent(self, response):
		"""
		De serialize response content
		"""
		return json.loads(response.content)

	def checkResponseRedirect(self, response):
		"""
		Check for redirection
		"""
		self.assertEqual(response.status_code, 302,
		                 "Server did not return 302 Redirect!!!")

	def test_1(self):
		"""
		Test for the following scenario -
		1) Provide a long url and gte the short url for it.
		2) Use the shortened url to get the actual url.
		3) Find the total number of time the short url was
		   used to access the long url
		"""

		long_url = 'https://www.hackerearth.com/challenge/hiring/hackerearth-python-developer-hiring-challenge/'

		data = {
			'long_url': long_url,
		}

		response = self.post(FETCH_SHORT_URL_ENDPOINT, data=data)

		# Check whether server return 200 OK
		self.checkResponseOK(response)

		# Get the data from the response
		response = self.getResponseContent(response)

		short_url = response['short_url']

		data = {
			"short_url": short_url,
		}

		response = self.post(FETCH_LONG_URL_ENDPOINT, data=data)

		# Check whether server return 200 OK
		self.checkResponseOK(response)

		response = self.getResponseContent(response)
		response_long_url = response['long_url']

		# Check whether the returned url matches the original url
		self.assertEqual(long_url, response_long_url, "Long url matching failed!!!")

		# Access the short URL thrice
		count = 1
		for _ in range(count):
			response = self.post(short_url, data={}, construct_url=False)

		data = {
			'short_url': short_url,
		}
		response = self.post(FETCH_COUNT_ENDPOINT, data=data)

		self.checkResponseOK(response)

		response = self.getResponseContent(response)

		response_count = response.get('count')
		if not response_count:
			raise Exception('Key Missing!')

		# Check whether URL access count matches with the expected value
		self.assertEqual(count, response_count, "URL access count did not match!!!")


	def test_2(self):
		"""
		Provide a list of complete urls and get the long urls.
		Provide the long url and get the short url.
		"""
		long_urls = [
			'https://www.hackerearth.com/challenge/hiring/hackerearth-python-developer-hiring-challenge/']

		data = {
			'long_urls': long_urls
		}

		response = self.post(FETCH_SHORT_URLS_ENDPOINT, data=data)

		# Check whether the returned url matches the original url
		self.checkResponseOK(response)

		response = self.getResponseContent(response)

		long_to_short_url_map = response['short_urls']

		short_urls = long_to_short_url_map.values()

		data = {
			"short_urls": short_urls,
		}

		response = self.post(FETCH_LONG_URLS_ENDPOINT, data=data)

		# Check whether the returned url matches the original url
		self.checkResponseOK(response)

		response = self.getResponseContent(response)
		long_urls = response['long_urls']

		# Check whether long urls match
		for url in long_urls:
			key = long_urls[url]
			self.assertEqual(
				long_to_short_url_map[key], url, "Long url matching failed!!!")


if __name__ == '__main__':
	TestURLShortener.url = sys.argv[1]
	sys.argv = sys.argv[:1]
	unittest.main()

