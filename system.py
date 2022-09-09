import json
import time
import requests
from requests import *
from datetime import datetime
from config import *
from tiktok_module import downloader

api = "https://api.telegram.org/bot" + token_bot
update_id = 0

def SendVideo(userid,msgid):
	tg_url = api + "/sendvideo"
	data = {
		"chat_id":userid,
		"caption":"<b>Лайк въебите за бота</b>",
		"parse_mode":"html",
		"reply_to_message_id":msgid,
		"reply_markup":json.dumps({
			"inline_keyboard":[
				[
					{
						"text":"like instagram",
						"url":"https://www.instagram.com/pawno.exe/"
					}
				]
			]
		})
	}
	res = post(
		tg_url,
		data=data,
		files={
			"video":open("video.mp4","rb")
		}
	)

def SendMsg(userid,text,msgid):
	tg_url = api + "/sendmessage"
	post(
		tg_url,
		json={
			"chat_id":userid,
			"text":text,
			"parse_mode":"html",
			"reply_to_message_id":msgid
		}
	)

def get_time(tt):
	ttime = datetime.fromtimestamp(tt)
	return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"

def Bot(update):
	try:
		global last_use
		userid = update['message']['chat']['id']
		meseg = update['message']['text']
		msgid = update['message']['message_id']
		timee = update['message']['date']
		dl = downloader.tiktok_downloader()
		if update['message']['chat']['type'] != "private":
			if "tiktok.com" in meseg and "https://" in meseg :
					getvid = dl.musicaldown(url=meseg,output_name="video.mp4")
					if getvid == False:
						SendMsg(
							userid,
							"<i>Failed to download video</i>\n\n<i>Try again later</i>",
							msgid
						)
						return
					elif getvid == "private/remove":
						SendMsg(
							userid,
							"<i>Failed to download video</i>\n\n<i>Video was private or removed</i>",
							msgid
						)
					elif int(len(open('video.mp4','rb').read()) / 1024) > 51200:
						SendMsg(
							userid,
							"<i>Failed to download video</i>\n\n<i>Video size to large</i>",
							msgid
						)
					elif getvid == 'url-invalid':
						SendMsg(
							userid,
							"<i>URL is invalid, send again !</i>",
							msgid)
					else:
						SendVideo(
							userid,
							msgid
						)
			return
		first_name = update['message']['chat']['first_name']
		print(f"{get_time(timee)}-> {userid} - {first_name} -> {meseg}")
		if meseg.startswith('/start'):
			SendMsg(
				userid,
				"<b>pers0nal1ty bot\n\nlink\n",
				msgid
			)
		elif "tiktok.com" in meseg and "https://" in meseg :
			getvid = dl.musicaldown(url=meseg,output_name="video.mp4")
			if getvid == False:
				SendMsg(
					userid,
					"<i>Failed to download video</i>\n\n<i>Try again later</i>",
					msgid
				)
				return
			elif getvid == "private/remove":
				SendMsg(
					userid,
					"<i>Failed to download video</i>\n\n<i>Video was private or removed</i>",
					msgid
				)
			elif int(len(open('video.mp4','rb').read()) / 1024) > 51200:
				SendMsg(
					userid,
					"<i>Failed to download video</i>\n\n<i>Video size to large</i>",
					msgid
				)
			elif getvid == 'url-invalid':
				SendMsg(
					userid,
					"<i>URL is invalid, send again !</i>",
					msgid)
			else:
				SendVideo(
					userid,
					msgid
				)
	except KeyError:
		return
