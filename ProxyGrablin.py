# -*- coding: utf-8 -*-

__title__ = "ProxyGrablin"
__description__ = "A simple proxy scraper and proxy checker with GUI."
__author__ = "DrPython3"
__contact__ = "https://github.com/DrPython3"
__date__ = "2024-10-03"
__version__ = "0.1"

"""
ProxyGrablin by DrPython3 (C) 2024

A simple and easy to use proxy scraper and checker with a GUI.

If you want to support this project, please consider a donation or tip me a coffee:

(BTC): 16KLyV8C1S9NGkPeaPTGZxahvh1uw9aQCv
(LTC): LboqWKdYjmVGu44kWkSSFTadVmzSu4B3sE

Every support is appreciated!

And do not forget to check the repository for Updates.
"""

# TODO: Add threading-support.
# TODO: Check logs and reduce to minimum.
# TODO: Integrate live output in GUI.

# Needed modules:
import sys
try:
	from PyQt5.QtWidgets import QApplication
	from PyQt5.QtWidgets import QWidget
	from PyQt5.QtWidgets import QPushButton
	from PyQt5.QtWidgets import QVBoxLayout
	from PyQt5.QtWidgets import QHBoxLayout
	from PyQt5.QtWidgets import QLabel
	from PyQt5.QtWidgets import QFileDialog
	from PyQt5.QtWidgets import QInputDialog
	from PyQt5.QtWidgets import QMessageBox
	from PyQt5.QtWidgets import QTextEdit
	from PyQt5.QtWidgets import QComboBox
	from PyQt5.QtWidgets import QSpinBox
	from PyQt5.QtGui import QPixmap
	from inc_scraper import scraper
	from inc_checker import checker
	from inc_etc import writer
	from inc_etc import logging
except:
	sys.exit("[ERROR] Cannot import needed modules.\n\n")

# ProxyGrablin:
class ProxyGrablin(QWidget):
	def __init__(self):
		super().__init__()
		# Needed variables:
		self.test_url = "http://www.google.com" # Standard URL for proxy checker
		self.selected_proxy_type = "http" # Standard proxy type for proxy checker
		self.timeout_value = 3 # Standard timeout for proxy checker
		self.initUI()

	def initUI(self):
		# GUI setup:
		main_layout = QHBoxLayout()
		control_layout = QVBoxLayout()

		# Logo:
		self.label = QLabel(self)
		pixmap = QPixmap("logo.png")
		self.label.setPixmap(pixmap)
		self.label.setScaledContents(True)
		self.label.resize(pixmap.width(), pixmap.height())
		control_layout.addWidget(self.label)

		self.label = QLabel("Simple Proxy Scraper & Checker v0.1", self)
		control_layout.addWidget(self.label)

		# Scraper button:
		self.scraper_button = QPushButton("Scrape Proxies", self)
		self.scraper_button.clicked.connect(self.proxy_scraper)
		control_layout.addWidget(self.scraper_button)

		# Test URL:
		self.label_url = QLabel(f"Test URL: {self.test_url}", self)
		control_layout.addWidget(self.label_url)

		# Test URL setting:
		self.set_url_button = QPushButton("Change test URL", self)
		self.set_url_button.clicked.connect(self.set_test_url)
		control_layout.addWidget(self.set_url_button)

		# Set proxy type for checker:
		self.proxy_type_label = QLabel("Set proxy type:", self)
		control_layout.addWidget(self.proxy_type_label)

		self.proxy_type_setting = QComboBox(self)
		self.proxy_type_setting.addItems(["http", "https", "socks4", "socks5"])
		self.proxy_type_setting.currentTextChanged.connect(self.set_proxy_type)
		control_layout.addWidget(self.proxy_type_setting)

		# Set timeout for checker:
		self.timeout_label = QLabel("Set default timeout (sec):", self)
		control_layout.addWidget(self.timeout_label)

		self.timeout_setting = QSpinBox(self)
		self.timeout_setting.setMinimum(1)
		self.timeout_setting.setMaximum(60)
		self.timeout_setting.setValue(self.timeout_value)
		self.timeout_setting.valueChanged.connect(self.set_timeout)
		control_layout.addWidget(self.timeout_setting)

		# Checker button:
		self.checker_button = QPushButton("Check Proxies", self)
		self.checker_button.clicked.connect(self.proxy_checker)
		control_layout.addWidget(self.checker_button)

		# Add Control_Layout to Main_Layout:
		main_layout.addLayout(control_layout)

		# Area for text output:
		self.result_display = QTextEdit(self)
		self.result_display.setReadOnly(True)
		main_layout.addWidget(self.result_display)

		# Build GUI:
		self.setLayout(main_layout)
		self.setWindowTitle("ProxyGrablin v0.1")
		self.show()

	def proxy_scraper(self):
		"""
		Scrapes potential proxy IPs from given URLs and saves all found unique
		IP addresses to a text file. URLs are read from a text file, too.
		URL file must provide one URL per line.
		:return: None
		"""
		scraped_ips = []
		unique_ips = []
		sources_to_scrape = 0
		sources_scraped = 0
		logging("Scraper started.")
		self.result_display.clear()
		self.result_display.append("Scraper started.")
		# Get file with URL list:
		urls, _ = QFileDialog.getOpenFileName(self, "Choose URL list for scraper", "", "Text Files (*.txt)")
		if urls:
			logging("Importing URL list.")
			# Import URL list from file:
			with open(urls, "r") as input_file:
				sources = [line.strip() for line in input_file.readlines()]
			# Scrape proxies from URLs:
			if sources:
				sources_to_scrape = len(sources)
				logging(f"Found {str(sources_to_scrape)} URLs to scrape.")
				for source in sources:
					sources_scraped += 1
					print(f"Scraping {str(sources_scraped)} of {str(sources_to_scrape)}: {source}")
					result = scraper(source)
					scraped_ips.extend(result)
			else:
				logging("No URLs to scrape.")
				self.result_display.append("No URLs to scrape.")
			# Remove duplicates from scraped data and fill unique_ips list:
			if len(scraped_ips) > 0:
				logging("Removing duplicate proxies.")
				print("Removing duplicate proxies.")
				ip_pool = set()
				for ip in scraped_ips:
					if ip not in ip_pool:
						unique_ips.append(ip)
						ip_pool.add(ip)
					else:
						continue
				try:
					del ip_pool
				except:
					pass
			# Save unique_ips list to file:
			if len(unique_ips) > 0:
				logging("Saving proxies to file.")
				output_file, _ = QFileDialog.getSaveFileName(self, "Save scraped IPs", "", "Text files (*.txt)")
				if output_file:
					writer(unique_ips, output_file)
					logging("Scraped proxies saved to file.")
					self.result_display.append("Scraped IPs saved to file.")
					print("Scraped proxies saved to file.")
				else:
					logging("Output file not specified.")
					self.result_display.append("Output file not specified.")
			else:
				logging("No proxies found.")
				self.result_display.append("No proxies found.")
		else:
			logging("No URLs to scrape.")
			self.result_display.append("No URLs to scrape.")

	def set_test_url(self):
		"""
		Used to set the URL which the proxy checker uses to test given proxies.
		:return: None
		"""
		logging("Setting new test URL.")
		new_url, ok = QInputDialog.getText(self, "Enter URL for checker", "Enter the URL for the checker:")
		if ok and new_url:
			self.test_url = new_url
			QMessageBox.information(self, "Test URL", f"New test URL set: {self.test_url}")
			logging("New test URL set.")
			self.result_display.append(f"New test URL set: {self.test_url}")
		else:
			QMessageBox.warning(self, "Invalid URL", "Entered URL is invalid, test URL not changed.")
			logging("Entered URL is invalid, test URL not changed.")
			self.result_display.append("Entered URL is invalid, test URL not changed.")
		self.label_url.setText(f"Test URL: {self.test_url}")

	def set_proxy_type(self, proxy_type):
		"""
		Used to set the proxy type the checker will test for.
		:param proxy_type: Proxy type used for the checker.
		:return: None
		"""
		self.selected_proxy_type = proxy_type
		logging(f"Proxy type to use set to {proxy_type}")
		self.result_display.append(f"Proxy type set to {proxy_type}")

	def set_timeout(self, value):
		"""
		Used to set the default timeout for the proxy checker.
		:param value: timeout in secounds
		:return: None
		"""
		self.timeout_value = value
		logging(f"Timeout value changed to {str(value)}")
		self.result_display.append(f"Timeout value changed to {str(value)}")
		self.timeout_label.setText(f"Timeout value changed to {str(value)}")

	def proxy_checker(self):
		"""
		Starts the proxy checker. IPs will be checked one by one. Working proxies
		are saved to a text file. The IPs to check have to be provided in a text file
		with one IP per line.
		:return: None
		"""
		working_proxies = []
		amount_ips = 0
		amount_proxies = 0
		self.result_display.clear()
		logging("Proxy Checker started.")
		self.result_display.append("Proxy Checker started - this will take some time. Please, be patient!")
		ips, _ = QFileDialog.getOpenFileName(self, "Choose file with proxy IPs", "", "Text files (*.txt)")
		# Get IPs from file:
		if ips:
			with open(ips, "r") as input_file:
				ips_to_check = [line.strip() for line in input_file.readlines()]
			amount_ips = len(ips_to_check)
			print(f"{str(amount_ips)} loaded for checking.")
			logging(f"{amount_ips} loaded for checking.")
			logging("Checking IPs ...")
			# Check every IP for working proxy:
			if ips_to_check:
				for ip in ips_to_check:
					result = checker(ip, self.selected_proxy_type, self.test_url, self.timeout_value)
					if "alive" in result:
						working_proxies.append(ip)
					print(result)
			else:
				self.result_display.append("No IPs to check.")
				logging("No IPs to check.")
			# Save working proxies to file:
			if working_proxies:
				amount_proxies = len(working_proxies)
				logging(f"Saving {str(amount_proxies)} {self.selected_proxy_type.upper()} proxies to file.")
				output_file, _ = QFileDialog.getSaveFileName(self, f"Save working {self.selected_proxy_type.upper()} proxies", "", "Text files (*.txt)")
				if output_file:
					writer(working_proxies, output_file)
					logging("Proxies saved to file.")
				else:
					logging("No output file specified.")
				# Show working proxies in GUI:
				self.result_display.clear()
				self.result_display.append("WORKING PROXIES:\n" + "-" * 25)
				for proxy in working_proxies:
					self.result_display.append(proxy)
			else:
				self.result_display.append("No working proxies found.")
				logging("No working proxies found.")
		else:
			logging("No file to load IPs from.")
			self.result_display.append("No file to load IPs from.")

# Main:
if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = ProxyGrablin()
	sys.exit(app.exec_())

# DrPython3 (C) 2024
