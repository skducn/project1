import cv2
import numpy as np

# 使用Python进行视频相似度比较实例
# 帧相似度>=0.85返回True，否则返回False


def pHash(img):
    # 获取图片哈希值
	# 缩放图片为32x32灰度图片
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_CUBIC)
	# 创建二维列表
	h, w = img.shape[:2]
	vis0 = np.zeros((h,w), np.float32)
	vis0[:h,:w] = img
	# 二维Dct变换
	vis1 = cv2.dct(cv2.dct(vis0))
	vis1 = vis1[:8, :8]
	# 把二维list变成一维list
	img_list = vis1.flatten().tolist()
	# 计算均值, 得到哈希值
	avg = sum(img_list) * 1. / 64
	avg_list = [0 if i < avg else 1 for i in img_list]
	return avg_list

def hanming_dist(s1, s2):
    # 求汉明距离
	return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])

def compare(video1: cv2.VideoCapture = None, video2: cv2.VideoCapture =None) -> bool:
	# 获取较短视频的帧数
	min_frame_count = min(video1.get(cv2.CAP_PROP_FRAME_COUNT),
							video2.get(cv2.CAP_PROP_FRAME_COUNT))
	# 获取视频FPS
	fps1 = video1.get(cv2.CAP_PROP_FPS)
	similar = 0
	frame_cnt = int(min_frame_count / fps1)
	# 截帧
	for _ in range(frame_cnt):
		for _ in range(int(fps1)): # 按视频一间隔1s
			retval1 = video1.grab()
			retval2 = video2.grab()
		if not retval1 or not retval2:
			grab_failure_cnt += 1
			if grab_failure_cnt >= 10:
				raise Exception('Grab failed too much >= {} times, could be endless loop.'.format(10))
		else:
			grab_failure_cnt = 0
		flag1, frame1 = video1.retrieve()
		flag2, frame2 = video2.retrieve()
		# 提phash特征
		if flag1 & flag2:
			phash1 = pHash(frame1)
			phash2 = pHash(frame2)
			# 比较汉明距离
			if hanming_dist(phash1, phash2) < 12:
				similar += 1
	print("similar:", similar/frame_cnt, frame_cnt)
	return similar / frame_cnt

def compareVideo(srcVideo, dstVideo):
	video1 = cv2.VideoCapture(srcVideo)
	video2 = cv2.VideoCapture(dstVideo)
	return compare(video1, video2)

a = compareVideo("/Users/linghuchong/Downloads/video/bilibili/test/test1/a1.mp4","/Users/linghuchong/Downloads/video/bilibili/test/test1/ff.mp4")
print(a)