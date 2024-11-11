# coding=utf-8
import os, sys
import shutil
import cv2
import cv2
import numpy as np
from PIL import Image
import math
import operator
from functools import reduce

'''此方法用于视频切割为图片，入参为切割的视频地址和输出的图片地址'''


def videoImage(dir_vieo, dir_image):
    # mp4存放的路径
    videos_src_path = dir_vieo
    # 保存的路径，会在路径下创建mp4文件名的文件夹保存图片
    videos_save_path = dir_image
    # 获取目标文件夹得视频列表，方便下面遍历
    videos = os.listdir(videos_src_path)

    for each_video in videos:

        # get the name of each video, and make the directory to save frames
        if ".mp4" in each_video:
            print('Video Name :', each_video)
            each_video_name, _ = each_video.split('.')
            url = videos_save_path + '/' + each_video_name
            if os.path.exists(url):
                # image的文件夹作为临时存储容器，清空用于保持文件夹得简洁性
                shutil.rmtree(url)
            os.mkdir(url)
            each_video_save_full_path = os.path.join(videos_save_path, each_video_name) + '/'
            # get the full path of each video, which will open the video tp extract frames
            each_video_full_path = os.path.join(videos_src_path, each_video)
            # cv2.VideoCapture()是用于从视频文件、图片序列、摄像头捕获视频并返回为cap对象
            cap = cv2.VideoCapture(each_video_full_path)
            # 第几帧
            frame_count = 1
            # 隔着多少帧取一张
            frame_rate = 200
            success = True
            # 计数
            num = 0
            while (success):
                # cap.read()进行读，cv2.imwrite()进行写，当读结束时，success变成False
                success, frame = cap.read()
                if success == True:
                    if frame_count % frame_rate == 0:
                        cv2.imwrite(each_video_save_full_path + each_video_name + "%03d.jpg" % num, frame)
                        num += 1
                frame_count = frame_count + 1
            print('image numbers:', num)


'''使用对比两张图片的差值判断图片是否相同，值为0则相同，值越大则差异越大'''


def compare(pic1, pic2):
    '''
    :param pic1: 图片1路径
    :param pic2: 图片2路径
    :return: 返回对比的结果
    '''
    if os.path.exists(pic1):
        pass
    else:
        raise IOError(f'图片不存在，请您仔细观察路径是否填写错误{pic1}')
    if os.path.exists(pic2):
        pass
    else:
        raise IOError(f'图片不存在，请您仔细观察路径是否填写错误{pic2}')
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)
    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(
        reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))
    if differ > 0 or differ < 0:
        return False
    if differ == 0:
        return True


'''判断两张图片是否有差异，有差异则把差异的部分合成一张图片，用于观察差异的部分'''


def equalImage(file1, file2):
    if os.path.exists(file1):
        pass
    else:
        raise IOError(f'图片不存在，请您仔细观察路径是否填写错误{file1}')
    if os.path.exists(file2):
        pass
    else:
        raise IOError(f'图片不存在，请您仔细观察路径是否填写错误{file2}')
    image1 = cv2.imread(file1)
    image2 = cv2.imread(file2)
    difference = cv2.subtract(image1, image2)
    result = not np.any(difference)  # if difference is all zeros it will return False

    if result is True:
        return True
    else:
        cv2.imwrite("./difference/result.jpg", difference)
        return False


'''此方法用于对比两个视频是否相同，为了清晰地说明技术，所以两个对比的视频名字需要一样'''


def equalsVideoVideo():
    dir_vs = '/Users/linghuchong/Downloads/video/bilibili/test/test1'
    dir_is = '/Users/linghuchong/Downloads/video/bilibili/test/test1/img'
    dir_vd = '/Users/linghuchong/Downloads/video/bilibili/test/test2'
    dir_id = '/Users/linghuchong/Downloads/video/bilibili/test/test2/img'
    # 使用自定义的方法对视频进行切割成多个图片
    videoImage(dir_vs, dir_is)
    videoImage(dir_vd, dir_id)
    # 遍历视频，对每个视频产生的图片进行对比
    for video in os.listdir(dir_vs):
        video_name, _ = video.split('.')
        source_list = os.listdir(f'{dir_is}/{video_name}')
        dect_list = os.listdir(f'{dir_id}/{video_name}')
        result = True
        for file1, file2 in zip(source_list, dect_list):
            result = compare(dir_is + '/' + video_name + '/' + file1, dir_id + '/' + video_name + '/' + file2)
            if result == False:
                result = False
        if result:
            print(f'两个视频:{video_name}.mp4一样')
        else:
            print(f'两个视频:{video_name}.mp4不一样')
        sys.exit(0)


if __name__ == '__main__':
    equalsVideoVideo()