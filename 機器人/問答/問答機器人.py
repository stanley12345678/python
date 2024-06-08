import pandas as pd
import random
import json
import re
from decimal import *
import os
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace

zenbo = pyzenbo.connect('192.168.12.64')
zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_listenLanguageId = 1
myUtterance = ''


def exit_function():
zenbo.robot.unregister_listen_callback()
zenbo.robot.set_expression(RobotFace.DEFAULT)
zenbo.release()
time.sleep(1)


def listen_callback(args):
global zenbo_speakSpeed, zenbo_speakPitch, zenbo_listenLanguageId, myUtterance
event_slu_query = args.get('event_slu_query', None)
if event_slu_query and event_slu_query.get('app_semantic').get('correctedSentence') and event_slu_query.get('app_semantic').get('correctedSentence') != 'no_BOS':
myUtterance = str(event_slu_query.get(
'app_semantic').get('correctedSentence'))
if event_slu_query and event_slu_query.get('error_code') == 'csr_failed':
myUtterance = ''


zenbo.robot.set_expression(RobotFace.DEFAULT)
time.sleep(int(0.5))
zenbo.robot.register_listen_callback(1207, listen_callback)
time.sleep(int(1))


qa_data = pd.read_excel("qa.xlsx", header=None)

q_count = 3
li = range(0, len(qa_data))

q_index = random.sample(li, q_count)

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, '我是問答機器人', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)


for i in range(q_count):
# print(qa_data.iloc[q_index[i]][0])
zenbo.robot.set_expression(RobotFace.PREVIOUS, qa_data.iloc[q_index[i]][0], {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
for k in range(1, 5):
for x in range(1, 5):
if((x == 1 and k == 1) or (x == 2 and k == 2) or (x == 3 and k == 3) or (x == 4 and k == 4)):
print(f'{k}{qa_data.iloc[q_index[i]][x]}')
zenbo.robot.set_expression(RobotFace.PREVIOUS, f'{k}{qa_data.iloc[q_index[i]][x]}', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
#q_item = " 一、"+qa_data.iloc[q_index[i]][1] + " 二、"+qa_data.iloc[q_index[i]][2] + " 三、"+qa_data.iloc[q_index[i]][3] + " 四、"+qa_data.iloc[q_index[i]][4]
# print(q_item)

zenbo_listenLanguageId = 1
zenbo.robot.speak_and_listen(
'請說出你的答案', {'listenLanguageId': zenbo_listenLanguageId})
time.sleep(int(3))

a = myUtterance
if a == qa_data.iloc[q_index[i]][5]:
# print("答對")

zenbo.motion.move_head(pitch_degree=-10, speed_level=2, sync=False)
zenbo.motion.move_head(pitch_degree=10, speed_level=2, sync=False)
zenbo.robot.set_expression(RobotFace.PREVIOUS, '答對', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)

else:
#print("答錯 " + "正確答案是 " + qa_data.iloc[q_index[i]][6])
zenbo.motion.move_body(relative_theta_degree=Decimal(
30), speed_level=2, sync=False)
zenbo.motion.move_body(
relative_theta_degree=Decimal(-60), speed_level=2, sync=False)
zenbo.motion.move_body(relative_theta_degree=Decimal(
30), speed_level=2, sync=False)
zenbo.robot.set_expression(RobotFace.LAZY, "答錯 " + "正確答案是 " + qa_data.iloc[q_index[i]][5] + qa_data.iloc[q_index[i]][6], {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)