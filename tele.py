import os
import time
import datetime
import telegram
from threading import Thread
# import test_runnner
from tele_const import *
from custom_logger import logger
from version import TargetVersion

class GlobalData:
	telegram_closed = False

class TelegramBot:
	def __init__(self):
		self._bot = telegram.Bot(token='498060301:AAEA4xoAMNLncQaFedQCIxAhRjHK03NVFhU')
		self._last_message = ''
		self._is_tests_running = False
		self._is_hello = False
		self._is_exit = False
		self._h = False
		self._last_checked_message = ''

	def _check_connection(self):
		print(bot.get_me())

	def _test_thread(self, dummy):
		test_runnner.main()
		self.send_message(m_test_finish)

	def _update_thread(self, dummy):
		while True:
			current_time = datetime.datetime.now().time()
			try:
				self._last_message = self._bot.get_updates()[-1].message.text
			except:
				logger.error('Exception during updating telegram data')
				pass
			try:
				cod = self._last_message.encode('utf8', 'ignore')
				# logger.info('Last message: ' + self._last_message)
				logger.info('Last message: ' + cod.decode())
			except:
				logger.error('Coding error')
				logger.info(self._last_message)
				pass

			if m_exit in self._last_message and not self._is_exit:
				self._is_exit = True
				GlobalData.telegram_closed = True
				logger.info('Get exit message')
				break

			if m_hello in self._last_message and not self._is_hello:
				self._is_hello = True
				self.send_message(m_hello)

			if m_tam in self._last_message and not self._h:
				self._h = True
				self.send_message(m_all_ok)

			if 'Шо на таргеті?' in self._last_message and self._last_message != self._last_checked_message:
				ver = TargetVersion()

				# qq = ver.get_version()
				# self.send_message(qq)

				try:
					qq = ver.get_version()
					self.send_message(qq)
				except:
					logger.error('FTP conenction error')
					self.send_message('FTP conenction error')

			if m_run_tests in self._last_message and not self._is_tests_running:
				logger.info('Start executing test runner')
				self._is_tests_running = True
				self.send_message(m_ok)
				test_thread = Thread(target=self._test_thread, args=(10,))
				test_thread.start()

			self._last_checked_message = self._last_message

			time.sleep(5)

	def send_message(self, message):
		logger.info('Send message: ' + message)
		chat_id = self._get_last_chat_id()
		if chat_id:
			self._bot.send_message(chat_id=self._get_last_chat_id(), text=message)
		else:
			logger.warning('chat id is empty')

	def _get_last_chat_id(self):
		# if not self._bot.get_updates():
		# 	return self._bot.get_updates()[-1].message.chat_id
		# return None
		return self._bot.get_updates()[-1].message.chat_id

	def run(self):
		thread = Thread(target=self._update_thread, args=(10,))
		thread.start()
		# time.sleep(1)
		# thread.join()



# def main():
bot = TelegramBot()
bot.run()

# main()
# if __name__ == '__main__':
# 	main()