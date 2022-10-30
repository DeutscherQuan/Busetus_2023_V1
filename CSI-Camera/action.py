#excute 1 action at specific time, only 1 time every mininute

import datetime
import time
now=datetime.datetime.now()

action_count =0
temp_min = -1

def action():
	print('Long')
	time.sleep(10)

def cond_action():
	now=datetime.datetime.now()
	if (now.minute%1==0 and action_count==0):
		return 1
	else:
		return 0
while 1:
	now=datetime.datetime.now()
	if (now.minute!=temp_min):
		action_count=0
	if cond_action() == 1:
		action()
		action_count =1
		temp_min= now.minute
