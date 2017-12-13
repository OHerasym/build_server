import os
import time
import datetime
import telegram
from threading import Thread
import test_runnner
from tele_const import *

class TelegramBot:
	def __init__(self):
		self._bot = telegram.Bot(token='498060301:AAEA4xoAMNLncQaFedQCIxAhRjHK03NVFhU')
		self._last_message = ''
		self._is_tests_running = False
		self._is_hello = False
		self._is_exit = False
		self._h = False

	def _check_connection(self):
		print(bot.get_me())

	def _test_thread(self, dummy):
		test_runnner.main()
		self.send_message(m_test_finish)

	def _update_thread(self, dummy):
		while True:
			current_time = datetime.datetime.now().time()
			self._last_message = self._bot.get_updates()[-1].message.text
			print('[' + str(current_time) + '] ' + self._last_message)

			if m_exit in self._last_message and not self._is_exit:
				self._is_exit = True
				break

			if m_hello in self._last_message and not self._is_hello:
				self._is_hello = True
				self.send_message(m_hello)

			if m_tam in self._last_message and not self._h:
				self._h = True
				self.send_message(m_all_ok)

			if m_run_tests in self._last_message and not self._is_tests_running:
				self._is_tests_running = True
				self.send_message(m_ok)
				test_thread = Thread(target=self._test_thread, args=(10,))
				test_thread.start()

			time.sleep(5)

	def send_message(self, message):
		self._bot.send_message(chat_id=self._get_last_chat_id(), text=message)

	def _get_last_chat_id(self):
		return self._bot.get_updates()[-1].message.chat_id

	def run(self):
		thread = Thread(target=self._update_thread, args=(10,))
		thread.start()
		time.sleep(1)



def main():
	bot = TelegramBot()
	bot.run()

if __name__ == '__main__':
	main()