import json
import re
import os
import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from pandas_datareader import data as pdr
from keras.models import Sequential
from keras.layers import Dense
import tensorflow

yf.pdr_override()
df = pd.read_csv("stock.csv")

zenbo = pyzenbo.connect('192.168.12.66')
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


def stockprice(stockid):
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/102.0.0.0 Safari/537.36'}
url = f"https://finance.yahoo.com/quote/{stockid}.TW?p={stockid}.TW"
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "lxml")
price = soup.find(
'fin-streamer', {'class': "Fw(b) Fz(36px) Mb(-4px) D(ib)"})
return price.text


def stockpredict(stockid):
data = pdr.get_data_yahoo(stockid + ".TW")
for i in range(len(data)):
if (data.Volume[i] == "0"):
data = data.drop[i]
hday = 400 # 歷史天數
df = pd.DataFrame()
df["open"] = data["Open"][-hday:]
df["high"] = data["High"][-hday:]
df["low"] = data["Low"][-hday:]
df["close"] = data["Close"][-hday:]
df["volume"] = data["Volume"][-hday:]

data_nor = df.apply(lambda x: (x-np.min(x))/(np.max(x))-(np.min(x)))
day = 1
data_tmp = data_nor.copy()
data_tmp2 = data_tmp["close"].iloc[day:]
data_tmp2 = data_tmp2.reset_index(drop=True)
data_tmp2.name = "after 1 day"
data_pre = data_tmp[-day:]
data_tmp1 = data_tmp[0:-day]
data_tmp1 = data_tmp1.reset_index(drop=True)
data_train = pd.concat([data_tmp1, data_tmp2], axis=1)

model = Sequential()
model.add(Dense(200, input_dim=5, activation="sigmoid"))
model.add(Dense(100, activation="sigmoid"))
model.add(Dense(1, activation="sigmoid"))
model.compile(loss="mean_squared_error", optimizer="adam",
metrics=["mean_squared_error"])
x_train = data_train.iloc[:, 0:5]
y_train = data_train.iloc[:, 5]
model.fit(x_train, y_train, epochs=1000, batch_size=200)
tomor = model.predict(data_pre)
data_min = np.min(df)
data_max = np.max(df)
tomor_price = tomor * \
(data_max["close"] - data_min["close"]) + data_min["close"]

return(str(tomor_price[0][0]))


zenbo.robot.set_expression(RobotFace.DEFAULT)
time.sleep(int(0.5))
zenbo.robot.register_listen_callback(1207, listen_callback)
time.sleep(int(1))

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, '我是股票機器人', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)

zenbo_listenLanguageId = 1
zenbo.robot.speak_and_listen(
'請問要查哪一支股票', {'listenLanguageId': zenbo_listenLanguageId})

time.sleep(int(3))

sn = myUtterance
while True:
if df["股票名稱"].str.contains(sn).any():
aa = df["股票代號"].loc[df["股票名稱"] == sn]
sid = '股價代號' + aa.values[0]
snow = '現在股價' + stockprice(aa.values[0])
sf = '明天股價' + stockpredict(aa.values[0])
break
else:
print("unexist")
sn = input("請輸入股票名稱:")

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, sid, {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
zenbo.robot.set_expression(RobotFace.PREVIOUS, snow, {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
zenbo.robot.set_expression(RobotFace.PREVIOUS, sf, {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
exit_function()
os._exit(0)
try:
while True:
time.sleep(int(10))
finally:
exit_function()