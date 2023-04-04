from datetime import datetime, date
from rich import print
from LuaWrapper import *

class Log:
	def print(message, without_dump_file = False):
		now = datetime.now()
		current_time = str(now.strftime("%H:%M:%S"))
		today = str(date.today())
		msg = f"[{current_time}] {message}"
		path = f"logs/dump-vnc-{today}.log"

		if without_dump_file == True:
			print(msg)
			return

		with open(path, 'a') as file:
			file.write(msg + "\n")
			print(msg)

	def printL(message, without_dump_file = False):
		now = datetime.now()
		current_time = str(now.strftime("%H:%M:%S"))
		today = str(date.today())
		msg = f"{message}"
		path = f"logs/dump-vnc-{today}.log"

		if without_dump_file == True:
			print(msg)
			return

		with open(path, 'a') as file:
			file.write(msg + "\n")
			print(msg)