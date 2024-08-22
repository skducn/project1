# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 抖音视频下载（手机端，Web端，支持单个视频、视频列表批量下载）
# 抖音 user_url 用户列表链接的获取方法：右上角...  - 分享 - 复制链接
# 手机版单视频页、列表页 https://v.douyin.com/Jp4GEo6/
# 网页版单视频页 https://www.douyin.com/discover
# 网页版列表页 https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg  全说商业

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣
#***************************************************************

import requests, re, os, platform, bs4, json, sys
import pyperclip as pc
from urllib import parse
# sys.path.append("../../../")
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")

# from PO.DataPO import *
# Data_PO = DataPO()
#
# from PO.FilePO import *
# File_PO = FilePO()
#
# from PO.HttpPO import *
# Http_PO = HttpPO()
#
from PO.StrPO import *
Str_PO = StrPO()

# from PO.WebPO import *
# Web_PO = WebPO("chrome")

class DyPO:

	def getVideo(self, surl, toPath):

		header = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"}

		# 解析获取id
		share = re.search(r'/v.douyin.com/(.*?)/', surl).group(1)
		share_url = "https://v.douyin.com/{}/".format(share)
		# print(share_url)  # https://v.douyin.com/SrL7RnM/
		s_html = requests.get(url=share_url, headers=header)
		surl = s_html.url
		print(surl)  # https://www.douyin.com/video/7352751321570757924
		if len(surl) > 60:
			id = re.search(r'video/(\d.*)/', surl).group(1)
		else:
			id = re.search(r'video/(\d.*)', surl).group(1)
		print(id) # 7206155470149635384

		#

		# 获取json数据
		u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&a_bogus=".format(id)
		# u_id = "https://m.douyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&item_ids={}&a_bogus=".format(id)

		print(u_id)
		v_rs = requests.get(url=u_id, headers=header)
		print(v_rs.json())
		sys.exit(0)
		# v_rs = requests.get(url=u_id, headers=header).json()
		# print(0,v_rs)

		# 作者名
		nickname = v_rs['item_list'][0]['author']['nickname']

		nickname = str(nickname).replace(" ", "_")
		print(1, nickname)

		# 视频标题
		titles = v_rs['item_list'][0]['desc']
		# print(3, v_rs['item_list'][0]['desc'])
		# titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc'])
		# titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
		# if titles == None:
		# 	titles = nickname
		# else:
		# 	titles = v_rs['item_list'][0]['desc']
		# 	titles = re.search(r'^(.*?)[；;。.#]', v_rs['item_list'][0]['desc']).group(1)
		# print(titles)

		# 创建video文件夹
		if not os.path.exists(toPath + nickname):
			os.makedirs(toPath + nickname)

		# 获取uri参数
		req = v_rs['item_list'][0]['video']['play_addr']['uri']
		# print("vvvvvv", req)

		# 下载无水印视频
		v_url = "https://www.douyin.com/aweme/v1/play/?video_id={}".format(req)
		v_req = requests.get(url=v_url, headers=header).content
		# print(v_url)
		print("下载中 ", v_url)
		# print(f"[下载中] => {v_url}")

		ff = toPath + nickname + "/" + titles + ".mp4"
		print(ff)

		# 写入文件
		with open(ff, 'wb') as f:
			f.write(v_req)

		print("[已完成] => ", ff)
		return toPath + nickname

	def getVideo2(self, surl, savePath):

		# 通过页面获取cookie（detail/？aweme_id=1644267442269561330）
		headers = {
			"cookie":
				"device_web_cpu_core=4; device_web_memory_size=8; __ac_nonce=065f3c1fa00bef1423f6; __ac_signature=_02B4Z6wo00f01yzcAJQAAIDCwvnEaoav5Nss.AQAAK7P9a; ttwid=1%7Cza3a0V9sZWVXQtFTYdg1tIYDQdKPXBCospMJtQBpJ28%7C1710473722%7C6aa9c4a695b158cfd9b251ef3152973d2c837476f809a67a376ebcccac4af056; csrf_session_id=6eaea5441cfead14775b47ceeacc531b; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; strategyABtestKey=%221710473724.647%22; passport_csrf_token=4de2dc6072fe1d0815862fb2675f0dc9; passport_csrf_token_default=4de2dc6072fe1d0815862fb2675f0dc9; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A1%7D; bd_ticket_guard_client_web_domain=2; ttcid=4518e71687614734b864141d15a00c0131; passport_assist_user=CjzIA27dVWnLf-9XbxwQESh4-y5q99AGtFnYJ2s24LrdfBIvOKTw6Y-VBQfVTqKrRscimoI0zTcA24xkYhoaSgo8srCHn7pW6sbKU1V6TQdQvMsQQp6FVbzfhX0aFPnn2Qy9ao8EfuoHmC3h85yZ1xZfxmkFAU9YPVEDUKFIEML8yw0Yia_WVCABIgEDbbeZjw%3D%3D; n_mh=WS535DN4ran5MY8jwy5rsPR32VTkVf71wiCo9CkZcUk; sso_uid_tt=883ae607e15aeed291f994a1aaffcfee; sso_uid_tt_ss=883ae607e15aeed291f994a1aaffcfee; toutiao_sso_user=1c4588c6e810a350e5646a7f4e98d4ab; toutiao_sso_user_ss=1c4588c6e810a350e5646a7f4e98d4ab; sid_ucp_sso_v1=1.0.0-KDBkZDU2OTkwNWNhMzhhODIwMzEzZjNjNWE2ZTExYTc5ODcyZTkxYTkKHQi-qf6o8AIQsYTPrwYY7zEgDDDyqITYBTgGQPQHGgJobCIgMWM0NTg4YzZlODEwYTM1MGU1NjQ2YTdmNGU5OGQ0YWI; ssid_ucp_sso_v1=1.0.0-KDBkZDU2OTkwNWNhMzhhODIwMzEzZjNjNWE2ZTExYTc5ODcyZTkxYTkKHQi-qf6o8AIQsYTPrwYY7zEgDDDyqITYBTgGQPQHGgJobCIgMWM0NTg4YzZlODEwYTM1MGU1NjQ2YTdmNGU5OGQ0YWI; passport_auth_status=a408ba0374e4cb9afaf790166e8accc2%2C; passport_auth_status_ss=a408ba0374e4cb9afaf790166e8accc2%2C; uid_tt=5f908ea1b85221f0c2344c01ecc7e059; uid_tt_ss=5f908ea1b85221f0c2344c01ecc7e059; sid_tt=f4e64b8da5fe064138ac91e75911983e; sessionid=f4e64b8da5fe064138ac91e75911983e; sessionid_ss=f4e64b8da5fe064138ac91e75911983e; publish_badge_show_info=%220%2C0%2C0%2C1710473783357%22; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=52e0d429df3a993303254e0224e054d0; __security_server_data_status=1; store-region=cn-sh; store-region-src=uid; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQ2trRjBXRUZhbkc4Z0Uzb3RoWHg4U3BFRE1qZUE0SVhUT2taVWFzSXF5N01DeW9TZFZxaEphaDNkUmRhSGFMMG1UT3VtUG1uZ2dBYmJDQi92azdGY0k9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; s_v_web_id=verify_lts3xhn6_tFhdD6mT_lVW3_4CEF_8TlA_LMEx6N3nIgO8; odin_tt=6bf7c94a6ce315b8b205796959e309edb6bf14135c801c7cb899c2470d4e1e003b39150696b1c8a6e5214408c6f42468; tt_scid=jaej88AxToHVzUSQXWDmNZziaZjc-evJLkLV6-MmY32zyh1TdIOtzrkjhERK.aQnec5d; d_ticket=c20707798d78785d2d8289658bd4806d5170f; sid_guard=f4e64b8da5fe064138ac91e75911983e%7C1710473803%7C5183978%7CTue%2C+14-May-2024+03%3A36%3A21+GMT; sid_ucp_v1=1.0.0-KGZlZGIyZTRlNmZkNGFkZDVjNDI4NDUwMTBiYTZjZDQwNGUxMmNiODMKGQi-qf6o8AIQy4TPrwYY7zEgDDgGQPQHSAQaAmxxIiBmNGU2NGI4ZGE1ZmUwNjQxMzhhYzkxZTc1OTExOTgzZQ; ssid_ucp_v1=1.0.0-KGZlZGIyZTRlNmZkNGFkZDVjNDI4NDUwMTBiYTZjZDQwNGUxMmNiODMKGQi-qf6o8AIQy4TPrwYY7zEgDDgGQPQHSAQaAmxxIiBmNGU2NGI4ZGE1ZmUwNjQxMzhhYzkxZTc1OTExOTgzZQ; msToken=Ew0cZ5gFbhaYNOu--GqDqFAgXKLFR2XnZBrJcujKcL1GcIFCeiU06MmEue3oI30p4B0UvWyv38Hc2kKCwUW77RLJqjWw2vrXk8bYNy0Z0lE6ZFkFnA2IWkXr6b4=; download_guide=%221%2F20240315%2F0%22; pwa2=%220%7C0%7C1%7C0%22; GlobalGuideTimes=%221710474233%7C1%22; msToken=gIX3RDGb5D1WOsUR5bZYG3qnp56Spn8JmJBaNmjRDobe5ZJHvlK7cCI2JiFKfBf6KndEslouBIViqmzljDA18w5zDLoDTcPSD9F5snaSMt2XuGSkl3ZbfrQ=; passport_fe_beating_status=false; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; dy_swidth=1440; dy_sheight=900; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAq9Lx60wscsSvp16gH6RYWZ3iyAngdi9YT0tgCXBbkQc%2F1710518400000%2F0%2F0%2F1710475404147%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAq9Lx60wscsSvp16gH6RYWZ3iyAngdi9YT0tgCXBbkQc%2F1710518400000%2F0%2F1710474804148%2F0%22",
				'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
		}

		# 获取id
		if "https://www.douyin.com/video/" not in surl:

			share = re.search(r'/v.douyin.com/(.*?)/', surl).group(1)
			share_url = "https://v.douyin.com/{}/".format(share)
			s_html = requests.get(url=share_url, headers=headers)
			surl = s_html.url
			# print(surl)  # https://www.douyin.com/video/7345754203735756069?previous_page=web_code_link
		id = surl.split("https://www.douyin.com/video/")[1].split("?")[0]
		# print(id)  # 7345754203735756069


		# 获取视频地址
		# 解析
		url = "https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={}".format(id)
		print(url)
		v_rs = requests.get(url=url, headers=headers).json()
		# print(v_rs)
		# 获取地址
		v_url = v_rs['aweme_detail']['video']['download_addr']['url_list'][0]
		# v_url = v_rs['aweme_detail']['video']['download_addr']['url_list'][3]
		# print(v_url)

		# 昵称（目录）
		v_nickname = v_rs['aweme_detail']['author']['nickname']
		v_nickname = str(v_nickname).replace(" ", "_").replace("(", "").replace(")", "")

		# 标题
		v_desc = v_rs['aweme_detail']['desc']
		v_desc = Str_PO.delSpecialChar(v_desc)


		# 3 下载视频
		result, pathFile = self.downVideo(v_url, v_nickname, v_desc, savePath)
		return (result, pathFile)


	def downVideo(self, v_url, v_folder, v_title,  savePath):
		'''
		1，下载单个抖音视频
		:param url = 'https://www.douyin.com/video/7157633339661307168'
		:param url = "https://v.douyin.com/hbjqhuT"
		'''

		# 创建video文件夹
		if not os.path.exists(savePath + v_folder):
			os.makedirs(savePath + v_folder)

		print("下载 => ", v_url)

		# 完整路径文件
		ff = savePath + v_folder + "/" + v_title + ".mp4"
		# print(ff)
		pathFile = savePath + v_folder + "/" + v_title

		# 写入文件
		res = requests.get(v_url)
		with open(ff, "wb") as f:
			f.write(res.content)

		print("[已完成] => ", ff)
		return (savePath + v_folder, pathFile)


	def save(self, varFolder, varTitle, varUrlSource, varExtension):
		'''
		1，下载单个抖音视频
		:param url = 'https://www.douyin.com/video/7157633339661307168'
		:param url = "https://v.douyin.com/hbjqhuT"
		'''
		# self.save(, author, filename, mp3)

		savePath = '/Users/linghuchong/Downloads/video/douyin/'

		# 创建文件夹
		if not os.path.exists(savePath + varFolder):
			os.makedirs(savePath + varFolder)

		# 完整路径文件
		varPath = savePath + varFolder
		ff = varPath + "/" + varTitle + varExtension

		# 写入文件
		# res = requests.get(varUrlSource)
		# with open(ff, "wb") as f:
		# 	f.write(res.content)

		res = requests.get(varUrlSource, stream=True)
		# print(res.status_code)  # 403的下载不了
		if res.status_code == 200:
			with open(ff, "wb") as f:
				for chunk in res.iter_content(chunk_size=8192):
					if chunk:
						f.write(chunk)


		print("[已完成] => ", ff)
		return varPath


	def getDetail(self, varExtension):

		# 通过剪贴板解析视频信息（打开抖音从detail中复制内容到剪贴板）
		string = pc.paste()
		data = json.loads(string)

		if data == '':
			# 通过detail.json 获取解析视频信息
			with open('/Users/linghuchong/Downloads/51/Python/project/instance/crawler/douyin/detail.json', 'r', encoding='utf-8-sig') as file:
				data = json.load(file)

		# https://www.douyin.com/video/7388545761698417920
		# print(data)

		aweme_id = data['aweme_detail']['aweme_id']  # 7388545761698417920
		# print(aweme_id)  # 7388545761698417920

		author = data['aweme_detail']['music']['author']
		print(author)  # 英语

		caption = data['aweme_detail']['caption']
		# print(caption)  # 在洗车场的对话，关于养宠物～鹦鹉#英语口语 #练口语 #英语 #听力 #生活英语
		filename = aweme_id + "，" + caption
		filename = Str_PO.delSpecialChar(filename)  # 7388545761698417920，在洗车场的对话，关于养宠物～鹦鹉#英语口语#练口语#英语#听力#生活英语
		print(filename)  # 7388545761698417920，在洗车场的对话，关于养宠物～鹦鹉#英语口语#练口语#英语#听力#生活英语

		url_mp3 = data['aweme_detail']['music']['play_url']['uri']
		print(url_mp3)  # https://sf5-hl-cdn-tos.douyinstatic.com/obj/ies-music/7388545888857180991.mp3

		url_mp4 = data['aweme_detail']['video']['download_addr']['url_list'][2]
		print(url_mp4)  # http://v3-web.douyinvod.com/e253e936b005b9e737ba7e795e08ff96/669a4e6e/video/tos/cn/tos-cn-ve-15/ooAXJUQgNrAFOEWZG49D6ifSfMDMABTI7iImoJ/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&br=695&bt=695&cs=0&ds=2&ft=pEaFx4hZffPdOW~-N12NvAq-antLjrK8CId.RkaypSmpUjVhWL6&mime_type=video_mp4&qs=0&rc=ZDg6aTY4NDwzNjxpODtoM0BpajRpNXc5cjhwdDMzNGkzM0AwNmFgMjQyNjMxLTZiYzA1YSNnbzZeMmQ0MzFgLS1kLWFzcw%3D%3D&btag=c0000e00038000&cquery=100o_100w_100B_100x_100z&dy_q=1721376986&feature_id=aec1901414fcc21744f0443229378a3c&l=20240719161626D25776EE6FED8C064CDA

		if varExtension == 'mp3':
			varPath = self.save(author, filename, url_mp3, '.mp3')
		elif varExtension == 'mp4':
			varPath = self.save(author, filename, url_mp4, '.mp4')

		return varPath


if __name__ == '__main__':

	Dy_PO = DyPO()

