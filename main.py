import os
import time
from datetime import datetime
from custom_logger import logger
from tele import bot
import builder
import rtc
import target_image



class GlobalValues:
	close_target_image = False


def get_and_build():
	_rtc = rtc.RTCConnect()
	_cluster = builder.ClusterHigh()
		#rtc.get_all_changes() # load workspace before
		#cluster.build_project()

		#cluster.clean_build()
	


def check_time():
	current_time = datetime.now()

	if current_time.minute == 0 and current_time.hour == 0:
		return True
	return False

def main():
	logger.info('Start execution')
	bot.send_message('Start execution')

	t_image = target_image.TargetImage()


	t_image.run()


	# while True:
	# 	print(check_time())
	# 	if check_time():
	# 		get_and_build()
	# 	time.sleep(30)




if __name__ == '__main__':
	main()