import cv2
import datetime
import time
import pyrebase
import sys
import urllib3
import signal

today = datetime.datetime.now()
config = {
  "apiKey": "AIzaSyDQzoT9FMh9wVGVLrF6oT8PUIaX8gOsMlQ",
  "authDomain": "test-5b0a6.firebaseapp.com",
  "databaseURL": "https://test-5b0a6-default-rtdb.firebaseio.com",
  "projectId": "test-5b0a6",
  "storageBucket": "test-5b0a6.appspot.com",
  "serviceAccount": "test_key.json"
  #"messagingSenderId": "656616970547",
  #"appId": "1:656616970547:web:8e3fff03575ab683078646",
  #"measurementId": "G-WXQGYY33DX" 
 }

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

def gstreamer_pipeline(
    sensor_id=0,
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

def handler(signum, frame):
	print("Forever is over!")
	raise Exception("end of time")

signal.signal(signal.SIGALRM, handler)

def show_camera():
    window_title = "/home/mlab/Downloads/CSI-Camera"
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
                if (today.minute % 1 == 0 and action_count == 0):
                    return 1
                else:
                    return 0
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)



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
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break
                # =========================
                if (today.minute != temp_min):
                    action_count = 0
                if cond_action() == 1:
                    today = datetime.datetime.now()
                    img_name = "{}.png".format(date_time)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_name = "{}.png".format(date_time) 
                    my_image = img_name
                    #time.sleep(3)

                    try:
                        signal.alarm(10)
                        img_name = "{}.png".format(date_time) 
                        my_image = img_name
                        #if internet_on():
                        storage.child(my_image).put(format(img_name))                         
                        action_count = 1
                        temp_min = today.minute
                        #print ("sent")
                        #time.sleep(1)
                        #else
                        signal.alarm(0)
                           #pass
                    except Exception as exc:
                        print(exc)
                        
                    
                    
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
