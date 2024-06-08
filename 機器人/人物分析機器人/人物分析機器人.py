import os
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
#from PIL import Image
from deepface import DeepFace
import cv2


zenbo = pyzenbo.connect('192.168.12.56')
record_picture_file = None
zenbo_speakSpeed = 100
zenbo_speakPitch = 100


def exit_function():
zenbo.robot.set_expression(RobotFace.DEFAULT)
zenbo.release()
time.sleep(1)


def on_result_callback(**kwargs):
global record_picture_file, zenbo_speakSpeed, zenbo_speakPitch
if kwargs.get('cmd') == commands.MEDIA_TAKE_PICTURE:
global record_picture_file
record_picture_file = kwargs.get('result').get('file')


e_d = {'angry': "生氣",
'disgust': "驗惡",
'fear': "恐懼",
'happy': "快樂",
'sad': "難過",
'surprise': "驚訝",
'neutral': "無表情"}
r_d = {'asian': "亞洲",
'indian': "印度",
'black': "非裔",
'white': "白種人",
'middle eastern': "中東",
'latino hispanic': "拉丁"}
g_d = {'Woman': "咖啡", 'Man': "男性"}


zenbo.robot.set_expression(RobotFace.DEFAULT)
time.sleep(int(0.5))
zenbo.on_result_callback = on_result_callback
time.sleep(int(1))

zenbo.media.take_picture()
time.sleep(int(1))
if record_picture_file is not None:
filePath, fileName = os.path.split(record_picture_file)
#zenbo.media.play_media(filePath, fileName, sync=False)
# time.sleep(int(1))
aa = zenbo.media.file_transmission(fileName)
#img = Image.open(aa[0])
# img.show()
img = cv2.imread(aa[0])
try:
emotions = DeepFace.analyze(img, actions=["emotion"])
ages = DeepFace.analyze(img, actions=["age"])
races = DeepFace.analyze(img, actions=["race"])
genders = DeepFace.analyze(img, actions=["gender"])
emotion = emotions[0]['dominant_emotion']
age = ages[0]['age']
race = races[0]['dominant_race']
gender = genders[0]['dominant_gender']
text = f"年紀:{age}歲 \n" + f"性別:{g_d[gender]} \n" + \
f"種族:{r_d[race]} \n" + f"表情:{e_d[emotion]} \n"

except:
test = "123"
pass


zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, text, {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
exit_function()
os._exit(0)
try:
while True:
time.sleep(int(10))
finally:
exit_function()