import cv2
import datetime
import time
import pyrebase
import sys
import urllib3
import os

import signal

def handler(signum, frame):
	print('Procedure is taking too long')
	raise Exception('Timed out after 20s')

signal.signal(signal.SIGALRM, handler)


today = datetime.datetime.now()
fb_state = False
path_to_directory = '/home/smarttrap/Desktop/Data/data'



# Declare Firebase address to connect to Python
config = {
  "apiKey": "AIzaSyCwBgvqH-j_TFMXijSNxnI2lC4f_l5zd3s",
  "authDomain": "smarttrap2022-9f9e7.firebaseapp.com",
  "databaseURL": "https://smarttrap2022-9f9e7-default-rtdb.firebaseio.com",
  "projectId": "smarttrap2022-9f9e7",
  "storageBucket": "smarttrap2022-9f9e7.appspot.com",
  "serviceAccount": "smarttrap2022key.json"
  #"messagingSenderId": "656616970547",
  #"appId": "1:656616970547:web:8e3fff03575ab683078646",
  #"measurementId": "G-WXQGYY33DX" 
 }


# This function try to initialize the app after taking picture. If already intialized, always return True
def init_fb_state():
	# Call global variables
	global storage
	global firebase_storage
	global fb_state

	if fb_state == False:
		try:
			firebase_storage = pyrebase.initialize_app(config)
			storage = firebase_storage.storage()
		except:
			print("No connection to firebase")
			fb_state = False
			return fb_state
	fb_state = True
	return fb_state
	

def internet_on():
	try:
	  url = 'http://www.google.com'
	  http = urllib3.PoolManager()
	  http.request ('GET', url, timeout = 5)
	  return True
	except urllib3.exceptions.HTTPError as err:
	  return False

def gstreamer_pipeline(
    sensor_id=0                                                         ,
    capture_width=1920,
    capture_height=1080,
    display_width= 960,    
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
	window_title = "/home/smarttrap/Desktop/CSI-Camera"
	today = datetime.datetime.now()
	print(gstreamer_pipeline(flip_method=0))
	video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
	if video_capture.isOpened():
		try:
			today = datetime.datetime.now()
			action_count = 0
			temp_min = -1

			def cond_action():
				today = datetime.datetime.now()
				# Change today.minute to change interval
				if (today.minute % 10 == 0 and action_count == 0):
					return 1
				else:
					return 0
	#  window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

			# This function is currently unused

			while True:
				today = datetime.datetime.now()
				date_time = today.strftime("%y%m%d%H%M")
				ret_val, frame = video_capture.read()

				keyCode = cv2.waitKey(10) & 0xFF
				if keyCode == 27 or keyCode == ord('q'):
					break

				if keyCode == ord('s'):
					img_name = "{}.png".format(date_time)
					cv2.imwrite(img_name, frame)
				# if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
				    # cv2.imshow(window_title, frame)
				# else:
				    # break
				# =========================
				if (today.minute != temp_min):
					action_count = 0
				if cond_action() == 1:
					today = datetime.datetime.now()
					img_name = "{}.png".format(date_time)
					full_name = os.path.join(path_to_directory, img_name)
					cv2.imwrite(full_name, frame)
					print("{} written!".format(img_name))
					print(format(full_name))
					if init_fb_state():	# Check if firebase is established
						print(fb_state)
						try:
							signal.alarm(20)	# Set up timer to 20s, limiting execution time
							# Declare variables and send image to Firebase Storage
							my_image = full_name
							storage.child(my_image).put(format(full_name)) 
							action_count = 1
							temp_min = today.minute
							time.sleep(1)

							#Get url of image and send it to Node-red
							auth = firebase_storage.auth()                
							email = 'quannm293@gmail.com'
							password = 'C2Deutsch'
							user = auth.sign_in_with_email_and_password(email, password)
							user = auth.refresh(user['refreshToken'])
							user['idToken']
							url = storage.child(my_image).get_url(user['idToken'])
							time.sleep(1)

							#Send url to firebase 
							firebase = pyrebase.initialize_app(config)
							database = firebase.database()
							x = database.child("Image URL Storage").push(url)
							database.child("Image URL Storage").get(x)             
							time.sleep(5)
							print(url)
							signal.alarm(0)
						except:
							signal.alarm(0)	# Set alarm to 0 to turn off the signal timer
							print('shit gone here')
							pass
					else:
						time.sleep(50)

		finally:
			video_capture.release()
			cv2.destroyAllWindows()

	else:
		print("Error: Unable to open camera")

if __name__ == "__main__":
	
    show_camera()	
                  

