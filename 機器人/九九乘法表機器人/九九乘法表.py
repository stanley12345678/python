import os
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
zenbo = pyzenbo.connect('192.168.12.61')
zenbo_speakSpeed = 100
zenbo_speakPitch = 100


def exit_function():
zenbo.robot.set_expression(RobotFace.DEFAULT)
zenbo.release()
time.sleep(1)


zenbo.robot.set_expression(RobotFace.DEFAULT)
time.sleep(int(0.5))
time.sleep(int(1))

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, '我是黃品心', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, '我來背九九乘法表', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
for i in range(2, 10):
for j in range(1, 10):
(print("%d * %d = %d" % (i, j, i*j)))
zenbo.robot.set_expression(RobotFace.PREVIOUS, "%d * %d = %d" % (i, j, i*j), {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
exit_function()
os._exit(0)
try:
while True:
time.sleep(int(10))
finally:
exit_function()