import logging, logging.handlers

class MyLogger:
	def logger_init():
		_logger = logging.getLogger('build_checker')
		_logger.setLevel(logging.DEBUG)

		fh = logging.FileHandler('example.log')
		fh.setLevel(logging.DEBUG)

		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# sh = logging.handlers.SocketHandler('172.31.220.71', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
		sh = logging.handlers.SocketHandler('0.0.0.0', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
		sh.setLevel(logging.DEBUG)

		formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] -  %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		_logger.addHandler(fh)
		_logger.addHandler(ch)
		_logger.addHandler(sh)

		return _logger

# print('[INFO] Logger init')
logger = MyLogger.logger_init()