import os
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
from deepface import DeepFace
import cv2

zenbo = pyzenbo.connect('192.168.')
record_picture_file = None
zenbo_speakSpeed = 100
zenbo_speakPitch = 100

name = {
"ma": "馬雲",
"mask": "瑪斯克",
"rock": "巨石強森",
"melon": "胡瓜",
"mo": "小萌"
}

def exit_function():
zenbo.robot.set_expression(RobotFace.DEFAULT)
zenbo.release()
time.sleep(1)

def on_result_callback(**kwargs):
global record_picture_file, zenbo_speakSpeed, zenbo_speakPitch
if kwargs.get('cmd') == commands.MEDIA_TAKE_PICTURE:
global record_picture_file
record_picture_file = kwargs.get('result').get('file')

zenbo.robot.set_expression(RobotFace.DEFAULT)
time.sleep(int(0.5))
zenbo.on_result_callback = on_result_callback
time.sleep(int(1))

zenbo.media.take_picture()
time.sleep(int(1))

if record_picture_file is not None:
filePath, fileName = os.path.split(record_picture_file)
zenbo.media.play_media(filePath, fileName, sync = False)
time.sleep(int(1))
aa = zenbo.media.file_transmission(fileName)
try:
df = DeepFace.find(img_path=aa,
db_path="zenboface/data", enforce_detection=True)
except:
msg = "err"
else:
msg = "ok"
dfname = name[df[0].loc[0][0].replace("\\", "/").split("/")[-2]]

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, dfname, {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
exit_function()
os._exit(0)
try:
while True:
time.sleep(int(10))
finally:
exit_function()