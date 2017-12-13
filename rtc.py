
import subprocess
import config
import time
from getpass import getpass
import base64


#TODO: change login and password to chaching


CREDENTIALS_FILE = "credantials"

class RTCConnect:
	def __init__(self):
		self._user = ''
		self._pasw = ''

	def _get_credantials(self):
		try:
			with open(CREDENTIALS_FILE, 'r') as fd:
				login = base64.b64decode(fd.readline().strip())
				passwd = base64.b64decode(fd.readline().strip())
				return login, passwd
		except(IOError):
			return None, None

	def _manual_login(self):
		self._user = input("RTC login: ")
		self._pasw = getpass('Password for {0}: '.format(self._user))
		
		# with open(CREDENTIALS_FILE, 'w') as credentials:
		# 	credentials.write(str(base64.b64encode(self._user.encode('utf-8'))))
		# 	# credentials.write(base64.b64encode(self._user))
		# 	credentials.write('\n')
		# 	credentials.write(str(base64.b64encode(self._pasw.encode())))

		return self._user, self._pasw

	def login(self):
		self._user, self._pasw = self._get_credantials()

		if not self._user:
			self._user, self._pasw = self._manual_login()

		subprocess.call(config.scm_path + ' ' + 'login -n local' + ' -u ' + self._user + ' ' + ' -P ' + self._pasw + ' -r ' + config.url_repository, shell=True)

	def load_workspace(self):
		subprocess.call(config.scm_path + 'load -r local -d ' + config.sources_dir + 
			' --remote-rules LoadRuleFiles/Streams/2.MFA2.DI.HMI.Integrity.DevEng/DI.HMI.DevEng_H2Integrity.loadrule --force target_build_802') 

	def accept(self):
		subprocess.call(config.scm_path + ' accept -r local -d ' + config.sources_dir + ' -v')

	def logout(self):
		subprocess.call(config.scm_path + ' logout -r local', shell=True)

	def get_all_changes(self):
		self.login()
		self.accept()
		self.logout()





def main():
	print(config.url_repository)

	rtc = RTCConnect()
	rtc.get_all_changes()


if __name__ == "__main__":
	main()