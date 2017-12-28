import sys
import os
import time
import pickle
import threading
from custom_logger import *
from tele import bot
from tele import GlobalData

from config import TargetImagesConfig as target_link

#TODO: add main loop

import urllib.request
import requests
from html.parser import HTMLParser


class TempState:
	close_target_image = False
	_image_link_is_set = False
	download_link = ''
	last_daily_high = ''
	last_daily_entry = ''
	last_release_high = ''
	last_release_entry = ''

	def init():
		try:
			with open('last_builds.txt', 'rb') as file:
				items = pickle.load(file)
				TempState.last_daily_high = items
				logger.info(TempState.last_daily_high)
				items = pickle.load(file)
				TempState.last_release_high = items
				logger.info(TempState.last_release_high)
				items = pickle.load(file)
				TempState.last_daily_entry = items
				logger.info(TempState.last_daily_entry)
				items = pickle.load(file)
				TempState.last_release_entry = items
				logger.info(TempState.last_release_entry)
		except FileNotFoundError:
			logger.warning('File last_builds.txt is empty or not exists!')

	def save():
		logger.info('Save builds to file')
		with open('last_builds.txt', 'wb') as file:
			pickle.dump(TempState.last_daily_high, file)
			pickle.dump(TempState.last_release_high, file)
			pickle.dump(TempState.last_daily_entry, file)
			pickle.dump(TempState.last_release_entry, file)

class MyHTMLParser(HTMLParser):
	def __init_(self):
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if 'a' == tag:
			if '_Images.7z' in attrs[0][1]:
				if TempState._image_link_is_set == False:
					logger.info('Last build: ' + attrs[0][1])
					TempState.download_link = attrs[0][1]
					TempState._image_link_is_set = True


class TargetImage:
	def __init__(self):
		self._images_folder = 'D:\\mfa2_images\\'
		self._stop_images_thread = False

	def _check_is_folder_exists(self, folder):
		if not os.path.exists(folder):
			os.makedirs(folder)
		
	def _reporthook(self,blocknum, blocksize, totalsize):
		readsofar = blocknum * blocksize
		if totalsize > 0:
			percent = readsofar * 1e2 / totalsize
			s = "\r%5.1f%% %*d / %d" % (
				percent, len(str(totalsize)), readsofar, totalsize)
			sys.stderr.write(s)
			if readsofar >= totalsize: # near the end
				sys.stderr.write("\n")
		else: # total size is unknown
			sys.stderr.write("read %d\n" % (readsofar,))


	def _check_all_folders(self):
		self._check_is_folder_exists(self._images_folder)
		self._check_is_folder_exists(self._images_folder + '\\Release\\')
		self._check_is_folder_exists(self._images_folder + '\\Daily\\')
		self._check_is_folder_exists(self._images_folder + '\\Release\\' + '\\High\\')
		self._check_is_folder_exists(self._images_folder + '\\Release\\' + '\\Entry\\')
		self._check_is_folder_exists(self._images_folder + '\\Daily\\' + '\\High\\')
		self._check_is_folder_exists(self._images_folder + '\\Daily\\' + '\\Entry\\')

	def _is_release_image(self, file_name):
		if 'Release' in file_name:
			return True
		return False

	def _is_high_image(self, file_name):
		if 'IC-H' in file_name:
			return True
		return False

	def _get_image_save_path(self, path):
		f = path
		if self._is_high_image(path):
			f = '\\High\\' + f
		else:
			f = '\\Entry\\' + f
		if self._is_release_image(path):
			f = '\\Release\\' + f
		else:
			f = '\\Daily\\' + f
		return f

	def download_image(self, image_link):
		self._check_all_folders()

		file_name = image_link.split('/')[-1]
		logger.info('Downloading file:' + file_name)
		bot.send_message('Downloading file: ' + file_name)

		# urllib.request.urlretrieve(image_link, self._images_folder + self._get_image_save_path(file_name), self._reporthook)
		urllib.request.urlretrieve(image_link, self._images_folder + self._get_image_save_path(file_name))

	def _read_page(self, jenkins_link):
		with urllib.request.urlopen(jenkins_link) as url:
			page = url.read()
		return page

	def _get_file_name(self, str):
		file_name = str.split('/')[-1]
		return file_name

	# def _check_last_build(self, build_value, link):
	# 	TempState._image_link_is_set = False # is set to True in HTMLParser

	# 	if build_value != self._get_file_name(link):
	# 		build_value = self._get_file_name(link)
	# 		return True
	# 	else:
	# 		logger.info('already last image')
	# 		return False

	def download_high_release(self):
		parser = MyHTMLParser()
		parser.feed(self._read_page(target_link.high_release_build).decode())

		TempState._image_link_is_set = False

		if TempState.last_release_high != self._get_file_name(target_link.high_release_build + TempState.download_link):
			TempState.last_release_high = self._get_file_name(target_link.high_release_build + TempState.download_link)
		else:
			logger.info('Already last image')
			return

		self.download_image(target_link.high_release_build + TempState.download_link)

	def download_high_daily(self):
		parser = MyHTMLParser()
		parser.feed(self._read_page(target_link.high_daily_build).decode())
		TempState._image_link_is_set = False

		if TempState.last_daily_high != self._get_file_name(target_link.high_daily_build + TempState.download_link):
			TempState.last_daily_high = self._get_file_name(target_link.high_daily_build + TempState.download_link)
		else:
			logger.info('Already last image')
			return

		self.download_image(target_link.high_daily_build + TempState.download_link)

	def download_entry_release(self):
		parser = MyHTMLParser()
		parser.feed(self._read_page(target_link.entry_release_build).decode())
		TempState._image_link_is_set = False

		if TempState.last_release_entry != self._get_file_name(target_link.entry_release_build + TempState.download_link):
			TempState.last_release_entry = self._get_file_name(target_link.entry_release_build + TempState.download_link)
		else:
			logger.info('Already last image')
			return

		self.download_image(target_link.entry_release_build + TempState.download_link)

	def download_entry_daily(self):
		parser = MyHTMLParser()
		parser.feed(self._read_page(target_link.entry_daily_build).decode())
		TempState._image_link_is_set = False

		if TempState.last_daily_entry != self._get_file_name(target_link.entry_daily_build + TempState.download_link):
			TempState.last_daily_entry = self._get_file_name(target_link.entry_daily_build + TempState.download_link)
		else:
			logger.info('Already last image')
			return

		self.download_image(target_link.entry_daily_build + TempState.download_link)

	def download_all(self):
		TempState.init()
		self.download_high_daily()
		self.download_high_release()
		self.download_entry_daily()
		self.download_entry_release()
		TempState.save()

	def _image_thread(self, dummy):
		while not self._stop_images_thread:
			self.download_all()
			time.sleep(10)
			if GlobalData.telegram_closed:
				self.stop()

	def stop(self):
		self._stop_images_thread = True

	def run(self):
		image_thread = threading.Thread(target=self._image_thread, args=(10,))
		image_thread.start()


def main():
	logger.info('Start execution!')
	target_image = TargetImage()
	target_image.run()

	# input()
	# target_image.stop()


if __name__ == '__main__':
	main()