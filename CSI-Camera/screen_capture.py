import os
import datetime


today = datetime.datetime.now()
date_time = today.strftime("%y%m%d%H%M")
print("date and time:",date_time)
string_time = str(date_time) + ".jpg"
path = "/home/jetson/catkin_ws/CSI-Camera/" + string_time

#os.system("gst-launch-1.0 nvarguscamerasrc num-buffers=1 ! 'video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1' ! nvjpegenc ! filesink location = " + path)
os.system("gst-launch-1.0 nvarguscamerasrc sensor_id=0 num-buffers=1 ! 'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! nvjpegenc ! filesink location = " + path)
#os.system("gst-launch-1.0 nvarguscamerasrc sensor_id=0 num-buffers=1 ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=1028, height=720' ! nvjpegenc ! filesink location = " + path)


