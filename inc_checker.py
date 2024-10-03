# -*- coding: utf-8 -*-

__title__ = "Proxy Checker for ProxyGrablin"
__description__ = "Checks given IPs for working proxies of a pre-defined type."
__author__ = "DrPython3"
__date__ = "2024-10-03"
__version__ = "0.1"
__contact__ = "https://github.com/DrPython3"

# TODO: Improve checker (geo info, anon level etc.).
# TODO: Prepare for threading.

# Needed modules:
import sys
import requests
from inc_etc import logging

# Functions:
def checker(ip_address, proxy_type, test_url, timeout_value):
	"""
	Checks a given proxy trying to open the given URL.
	:param ip_address: IP of the proxy
	:param proxy_type: HTTP, HTTPS, SOCKS4 or SOCKS5
	:param test_url: URL for connection test
	:param timeout_value: timeout for connection test
	:return: proxy information (text)
	"""
	if "socks" in proxy_type:
		proxy_url = f"{proxy_type}h://{ip_address}"
	else:
		proxy_url = f"{proxy_type}://{ip_address}"
	proxy = {proxy_type: proxy_url}
	try:
		logging(f"Checking {proxy_type.upper()} proxy {ip_address}.")
		response = requests.get(test_url, proxies=proxy, timeout=timeout_value)
		if response.status_code == 200:
			logging(f"{proxy_type.upper()} proxy {ip_address} is alive.")
			return f"{proxy_type.upper()} proxy {ip_address} is alive."
		else:
			logging(f"{proxy_type.upper()} proxy {ip_address} returns errors.")
			return f"{proxy_type.upper()} proxy {ip_address} returns errors."
	except:
		logging(f"{proxy_type.upper()} proxy {ip_address} is dead.")
		return f"{proxy_type.upper()} proxy {ip_address} is dead."

# DrPython3 (C) 2024
