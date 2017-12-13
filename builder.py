import os
import sys
import config
import subprocess
from colorama import init
import time
import shutil
import signal
from threading import Thread

#TODO: implement ClusterEntry
#TODO: calculate time to end (sqlite3)

#TODO: save and return previous directory

AMG = 'X86Win.Dbg.DI.E02x.SIMU'
CARS = 'X86Win.Dbg.DI.SIMU'

build = [CARS, AMG]
build_time = [13, 13, 1200, 1200, 680]

class ClusterHigh:
	def __init__(self, amg = True):
		self._is_amg = amg
		self._build_log = 'build_log.log'
		self._gen_1_log = 'gen_1.log'
		self._gen_2_log = 'gen_2.log'
		self._server_log = 'server.log'
		self._client_log = 'cluster_high.log'
		self._disp_log = 'disp.log'
		self._error_log = 'errors.log'
		self._build_finished = False
		self._build_result = False
		self._total_time = None

	def __build_thread(self, command, logging):
		error_log = open(self._error_log, 'w+')

		self._build_result = subprocess.call(command, shell=True, stdout=logging, stderr=error_log)

		self._build_finished = True
		error_log.close()

	def __build(self, command, log, print_string, build_time):
		init()
		os.chdir(config.sources_dir)
		logging = open(log, 'w')

		start_time = time.time()
		print(' [  BUILD  ]  ' + print_string + '\r', flush=True, end='')
		build_thread = Thread(target=self.__build_thread, args=(command, logging))
		build_thread.start()

		def get_time_str(time):
			if time > 100:
				return ' ' + str(100)
			if time < 10:
				return '  ' + str(time)
			else:
				return ' ' + str(time)

		while not self._build_finished:
			time.sleep(0.2)
			t = time.time() - start_time
			rr = t / build_time

			time_str = get_time_str(int(rr * 100))

			print(' [  ' +  time_str + ' %  ]  ' + print_string + '\r', flush=True, end='')

		build_thread.join()
		self._build_finished = False

		end_time = time.time() - start_time

		if self._build_result:
			print('\033[31m [  FAIL  ] \033[0m ' + print_string + ' ( %d s )' % end_time)
		else:
			print('\033[92m [ SUCCESS ] \033[0m '+ print_string + ' ( %d s )' % end_time)

		logging.close()

	def _generate_data(self):
		self.__build('uic_data_gen.bat X86Win.Dbg.DI.SIMU SM_UIConfig_DI', self._gen_1_log, 'uic_data_gen.bat', build_time[0])

	def _generate_conf(self):
		self.__build('uic_static_conf.bat X86Win.Dbg.DI.SIMU SM_UIConfig_DI', self._gen_2_log, 'uic_static_conf.bat', build_time[1])

	def _build_server(self):
		self.__build('s.bat ' + build[self._is_amg], self._server_log, 'server', build_time[2])

	def _build_client(self):
		self.__build('h.bat ' + build[self._is_amg], self._client_log, 'ClusterHigh', build_time[3])

	def _build_dispatcher(self):
		self.__build('Tools\\Bunny\\Bunny\\bin\\BunnyBuild HMISimulation.DispatcherProcess '+ build[self._is_amg],
			self._disp_log, 'DispatcherProcess', build_time[4])

	def _remove_dir(self, directory):
		try:
			shutil.rmtree(config.sources_dir +  directory)
		except FileNotFoundError:
			print('[INFO]: ' + directory + ' is already removed')

	def clean_build(self):
		self._remove_dir('\\ProductSpace')
		self._remove_dir('\\InterSpace')

	def build_project(self):
		self._generate_data()
		self._generate_conf()
		self._build_server()
		self._build_client()
		self._build_dispatcher()



def main():
	print(config.sources_dir)

	cluster = ClusterHigh()

	cluster.build_project()
	# cluster.clean_build()

if __name__ == '__main__':
	main()