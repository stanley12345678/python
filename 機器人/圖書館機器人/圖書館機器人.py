

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, '我是圖書館機器人', {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)


zenbo.media.take_picture()
time.sleep(int(1))
if record_picture_file is not None:
filePath, fileName = os.path.split(record_picture_file)
#zenbo.media.play_media(filePath, fileName, sync = False)
# time.sleep(int(1))
aa = zenbo.media.file_transmission(fileName)
img = cv2.imread(aa[0])
bd = cv2.barcode.BarcodeDetector()
retval, decode_info, decode_type, points = bd.detectAndDecode(img)
if retval:
barcode = decode_info[0]
url = f"https://books.google.com.tw/books?vid=ISBN{barcode}&redir_esc=y"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/102.0.0.0 Safari/537.36'}
r = requests.get(url, headers=headers)
r.text
txt = BeautifulSoup(r.text, "html.parser")
txt2 = txt.find_all("title")
txt3 = txt2[0].text
txt4 = txt3.split(" - ")
text = f"我要導讀《書名:{txt4[0]} , 作者:{txt4[1]}》這本書，可否為我摘要這本書50個字的閱讀心得"
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "你是有用的助理"},
{"role": "user", "content": text}
]
)

else:
print("no find")

zenbo_speakLanguage = 1
zenbo.robot.set_expression(RobotFace.PREVIOUS, response["choices"][0]["message"]["content"].replace("\n", ""), {
'speed': zenbo_speakSpeed, 'pitch': zenbo_speakPitch, 'languageId': zenbo_speakLanguage}, sync=True)
exit_function()
os._exit(0)
try:
while True:
time.sleep(int(10))
finally:
exit_function()
