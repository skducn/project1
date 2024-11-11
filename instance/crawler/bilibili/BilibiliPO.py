# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-28
# Description: bilibili视频下载

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣

# json在线解析 https://www.sojson.com/
# js在线解密 https://www.sojson.com/jsjiemi.html
# 5分钟学会用python爬取b站视频 https://www.bilibili.com/read/cv16789932/

# 问题：× Cannot uninstall decorator 5.1.1
# ╰─> The package's contents are unknown: no RECORD file was found for decorator.
# pip3 install moviepy
# pip3 install --ignore-installed decorator

# todo 下载1080视频，需要登录后获取cookies 方法如下：
# 1，先手机安装bilibili客户端，并登录
# 2，执行getCookies.py脚本，弹出二维码，微信扫描后生成cookies，并保存在cookies.txt
# 3，BilibiliPO.py - download_video中的request中加入cookies
# 如：cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b', 'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC', 'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b', 'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}
# request.get(url,header=header,cookies=cookies)
#***************************************************************

import sys, subprocess, json
sys.path.append("../../../")


from bs4 import BeautifulSoup

import time
import requests
import json
import re
from lxml import etree
from moviepy.editor import *




class BilibiliPO:

	def getBvidStr(self, jump_url):
		varPreUrl = "https://www.bilibili.com/video/"
		jump_url = varPreUrl + jump_url
		# print('页面：', jump_url)
		# 发送请求
		cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b',
				   'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC',
				   'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b',
				   'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}

		headers = {
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
		}

		response = requests.get(jump_url, headers=headers, cookies=cookies)

		# 视频内容json
		match = re.search(r'__INITIAL_STATE__=(.*?);\(function\(\)', response.text)
		initial_state = json.loads(match.group(1))
		len_count = len(initial_state['videoData']['ugc_season']['sections'][0]['episodes'])
		s = ''
		for i in range(len_count):
			s = s + "," + initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['bvid']
		return s

	def getBvid(self, jump_url):
		varPreUrl = "https://www.bilibili.com/video/"
		jump_url = varPreUrl + jump_url
		print('页面：', jump_url)
		# 发送请求
		cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b',
				   'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC',
				   'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b',
				   'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}

		headers = {
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
		}

		response = requests.get(jump_url, headers=headers, cookies=cookies)
		# print("response =>",response.text)

		# 视频内容json
		match = re.search(r'__INITIAL_STATE__=(.*?);\(function\(\)', response.text)
		initial_state = json.loads(match.group(1))
		# print("initial_state: => " , initial_state)

		s_ugc_season_title = initial_state['videoData']['ugc_season']['title']
		s_ownerName = initial_state['videoData']['owner']['name']

		len_count = len(initial_state['videoData']['ugc_season']['sections'][0]['episodes'])
		d_ = {}
		d_2 = {}
		d_2['ownerName'] = s_ownerName
		d_2['s_ugc_season_title'] = s_ugc_season_title
		for i in range(len_count):
			# print(initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['title'], initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['bvid'])

			title = initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['title']
			title = title.replace("/", "|")
			d_[initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['bvid']] = title
		d_2['data'] = d_
		return d_2

	def merge_video_audio(self, video_path, audio_path):
		# 获取下载好的音频和视频文件
		vd = VideoFileClip(video_path)
		ad = AudioFileClip(audio_path)
		vd2 = vd.set_audio(ad)  # 将提取到的音频和视频文件进行合成
		output = video_path.replace('_video', '')
		vd2.write_videofile(output)  # 输出新的视频文件

		# 移除原始的视频和音频
		os.remove(video_path)
		os.remove(audio_path)

	def downloadMore(self, jump_url):

		varPreUrl ="https://www.bilibili.com/video/"
		jump_url = varPreUrl + jump_url
		print('下载地址：', jump_url)
		# 发送请求
		cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b',
				   'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC',
				   'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b',
				   'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}

		headers = {
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
		}

		response = requests.get(jump_url, headers=headers,cookies=cookies)
		# print("response =>",response.text)
		# sys.exit(0)
		# 视频详情json
		match = re.search('__playinfo__=(.*?)</script><script>', response.text)
		playinfo = json.loads(match.group(1))
		# print("playinfo: => " , playinfo)

		# 视频内容json
		match = re.search(r'__INITIAL_STATE__=(.*?);\(function\(\)', response.text)
		initial_state = json.loads(match.group(1))
		# print("initial_state: => " , initial_state)

		len_count = len(initial_state['videoData']['ugc_season']['sections'][0]['episodes'])
		# print(len_count)
		d_ = {}
		for i in range(len_count):
			# print(initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['title'], initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['bvid'])
			d_[initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['bvid']] = initial_state['videoData']['ugc_season']['sections'][0]['episodes'][i]['title']


		# 视频分多种格式，直接取分辨率最高的视频 1080p
		video_url = playinfo['data']['dash']['video'][0]['baseUrl']
		# 取出音频地址
		audio_url = playinfo['data']['dash']['audio'][0]['baseUrl']
		title = initial_state['videoData']['title']
		bvid = initial_state['videoData']['bvid']

		name = initial_state['videoData']['owner']['name']
		title = title.replace("/", "|")
		title = bvid + "_" + title
		# print('视频名字：', title)
		# print('发布者（目录）：', name)
		# print('视频地址：', video_url)
		# print('音频地址：', audio_url)

		keyword = "/Users/linghuchong/Downloads/video/bilibili/" + name

		# 根据关键词创建文件夹
		if not os.path.exists(keyword):
			os.mkdir(keyword)

		varFile = title + ".mp4"
		for s_path, l_folder, l_file in os.walk(keyword):
			# print(l_file)
			if varFile not in l_file:
				# 下载视频
				headers.update({"Referer": jump_url})
				video_content = requests.get(video_url, headers=headers)
				received_video = 0
				video_path = f'{keyword}/{title}_video.mp4'
				with open(video_path, 'ab') as output:
					while int(video_content.headers['content-length']) > received_video:
						headers['Range'] = 'bytes=' + str(received_video) + '-'
						response = requests.get(video_url, headers=headers)
						output.write(response.content)
						received_video += len(response.content)

				# 下载音频
				audio_content = requests.get(audio_url, headers=headers)
				received_audio = 0
				audio_path = f'{keyword}/{title}_audio.mp4'
				with open(audio_path, 'ab') as output:
					while int(audio_content.headers['content-length']) > received_audio:
						# 视频分片下载
						headers['Range'] = 'bytes=' + str(received_audio) + '-'
						response = requests.get(audio_url, headers=headers)
						output.write(response.content)
						received_audio += len(response.content)

				# 合并视频和音频
				# print(video_path)
				# print(audio_path)
				self.merge_video_audio(video_path, audio_path)
				print('********************这是一条隔离线***************************')

				time.sleep(1)
			else:
				print("[warning]", varFile + " 已存在！")

	def downloadOne(self, jump_url):

		varPreUrl ="https://www.bilibili.com/video/"
		jump_url = varPreUrl + jump_url
		print('视频地址：', jump_url)
		# 发送请求
		cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b',
				   'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC',
				   'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b',
				   'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}

		headers = {
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
		}

		response = requests.get(jump_url, headers=headers,cookies=cookies)
		# print("response =>",response.text)
		# sys.exit(0)
		# 视频详情json
		match = re.search('__playinfo__=(.*?)</script><script>', response.text)
		playinfo = json.loads(match.group(1))
		# print("playinfo: => " , playinfo)

		# 视频内容json
		match = re.search(r'__INITIAL_STATE__=(.*?);\(function\(\)', response.text)
		initial_state = json.loads(match.group(1))
		# print("initial_state: => ", initial_state)


		# 视频分多种格式，直接取分辨率最高的视频 1080p
		video_url = playinfo['data']['dash']['video'][0]['baseUrl']
		# 取出音频地址
		audio_url = playinfo['data']['dash']['audio'][0]['baseUrl']
		title = initial_state['videoData']['title']
		bvid = initial_state['videoData']['bvid']

		name = initial_state['videoData']['owner']['name']
		title = title.replace("/", "|")
		title = bvid + "_" + title
		# print('视频名：', title)
		# print('发布者（目录）：', name)
		# print('视频地址：', video_url)
		# print('音频地址：', audio_url)

		keyword = "/Users/linghuchong/Downloads/video/bilibili/" + name

		# 检查本地路径视频是否存在

		# 根据关键词创建文件夹
		if not os.path.exists(keyword):
			os.mkdir(keyword)

		varFolder = "/Users/linghuchong/Downloads/video/bilibili/" + name
		varFile = title + ".mp4"
		for s_path, l_folder, l_file in os.walk(varFolder):
			# print(l_file)
			if varFile not in l_file:
				# print(111)
				# 下载视频
				headers.update({"Referer": jump_url})
				video_content = requests.get(video_url, headers=headers)
				received_video = 0
				video_path = f'{keyword}/{title}_video.mp4'
				with open(video_path, 'ab') as output:
					while int(video_content.headers['content-length']) > received_video:
						headers['Range'] = 'bytes=' + str(received_video) + '-'
						response = requests.get(video_url, headers=headers)
						output.write(response.content)
						received_video += len(response.content)

				# 下载音频
				audio_content = requests.get(audio_url, headers=headers)
				received_audio = 0
				audio_path = f'{keyword}/{title}_audio.mp4'
				with open(audio_path, 'ab') as output:
					while int(audio_content.headers['content-length']) > received_audio:
						# 视频分片下载
						headers['Range'] = 'bytes=' + str(received_audio) + '-'
						response = requests.get(audio_url, headers=headers)
						output.write(response.content)
						received_audio += len(response.content)

				# 合并视频和音频
				# print(video_path)
				# print(audio_path)
				self.merge_video_audio(video_path, audio_path)
				print('********************这是一条隔离线***************************')

				time.sleep(1)
			else:
				print("[warning]", name, varFile + " 已存在！")
	def downAll(self, d_):

		varFolder = "/Users/linghuchong/Downloads/video/bilibili/" + d_['ownerName']
		for s_path, l_folder, l_file in os.walk(varFolder):
			...
		# print(len(l_file))

		for k, v in d_['data'].items():
			fileName = k + "_" + v + ".mp4"
			if fileName not in l_file:
				self.downloadMore(k)
			else:
				print(fileName)


if __name__ == '__main__':

	Bilibili_PO = BilibiliPO()

	# Bilibili_PO.downloadVideo(["BV1et421g71W"])
	print(Bilibili_PO.getBvid('BV1et421g71W'))