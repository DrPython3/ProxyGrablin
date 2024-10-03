# -*- coding: utf-8 -*-

__title__ = "Scraper for ProxyGrablin"
__description__ = "Scrapes proxies from given websites."
__author__ = "DrPython3"
__date__ = "2024-10-03"
__version__ = "0.1"
__contact__ = "https://github.com/DrPython3"

# Needed modules:
import sys
import re
import requests
from inc_etc import logging

# Functions:
def scraper(url):
	"""
	Scrapes IPs from given URL and returns a list.
	:param url: URL to scrape
	:return: IP list
	"""
	ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}\b"
	try:
		logging(f"Scraping: {url}")
		response = requests.get(url)
		response.raise_for_status()
		scraped = response.text
		ips = re.findall(ip_regex, scraped)
		logging(f"Scraped {url} successfully.")
		return ips
	except requests.RequestException as e:
		logging(f"Scraping {e} failed.")
		return []

# DrPython3 (C) 2024
