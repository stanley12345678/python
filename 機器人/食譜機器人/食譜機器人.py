import json
import re
import os
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
import googletrans
from translate import Translator
import openai
openai.api_key = "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"

zenbo = pyzenbo.connect('192.168.12.66')
zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_listenLanguageId = 1
myUtterance = {'', ''}


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
myUtterance = {'', ''}


zenbo.robot.set_expression(RobotFace.DEFAULT)
time.sleep(int(0.5))
zenbo.robot.register_listen_callback(1207, listen_callback)
time.sleep(int(1))

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, '請問您的材料有哪些:', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
zenbo_listenLanguageId = 1
zenbo.robot.speak_and_listen(
{"", ""}, {'listenLanguageId': zenbo_listenLanguageId})
time.sleep(int(5))
print(myUtterance)

response = openai.Completion.create(
model="text-davinci-003",
prompt="Write a recipe based on these ingredients and instructions:\n\nIngredients:\n" +
myUtterance+"\n\nInstructions:",
temperature=0.3,
max_tokens=500,
top_p=1.0,
frequency_penalty=0.0,
presence_penalty=0.0
)
aa = response.choices[0].text
print(aa)

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, myUtterance, {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
response = openai.Completion.create(
model="text-davinci-003",
prompt="Translate this into 1. Chinese:\n\n"+aa+" \n\n1.",
temperature=0.3,
max_tokens=500,
top_p=1.0,
frequency_penalty=0.0,
presence_penalty=0.0
)
aa1 = response.choices[0].text
print(aa1)
zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, aa1, {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
exit_function()
os._exit(0)
try:
while True:
time.sleep(int(10))
finally:
exit_function()