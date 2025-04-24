# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description:

# import pymkv
#
# def extract_subtitles_from_mkv(mkv_file_path, output_path):
#     mkv = pymkv.MKVFile(mkv_file_path)
#     # 遍历所有字幕轨道
#     for track in mkv.tracks:
#         if track.track_type == 'subtitles' and track.language == 'eng':  # 假设提取英文字幕
#             mkv.extract_subtitles(track.id, output_path)
#             print(f"字幕已提取到 {output_path}")
#             return
#     print("未找到英文字幕轨道。")
#
# # 使用示例
# mkv_file = '/Users/linghuchong/Downloads/video/douyin/7473424691760254260.mkv'
# output_file = 'extracted_subtitles.srt'
# extract_subtitles_from_mkv(mkv_file, output_file)



import pymkv

# 手动指定 mkvmerge 的路径
pymkv.MKVFile.set_global_mkvmerge_path('/usr/local/bin/mkvmerge')

def extract_subtitles_from_mkv(mkv_file_path, output_path):
    mkv = pymkv.MKVFile(mkv_file_path)
    # 遍历所有字幕轨道
    for track in mkv.tracks:
        if track.track_type == 'subtitles' and track.language == 'eng':  # 假设提取英文字幕
            mkv.extract_subtitles(track.id, output_path)
            print(f"字幕已提取到 {output_path}")
            return
    print("未找到英文字幕轨道。")

# 使用示例
# mkv_file = 'your_video.mkv'
mkv_file = '/Users/linghuchong/Downloads/video/douyin/7473424691760254260.mkv'

output_file = 'extracted_subtitles.srt'
extract_subtitles_from_mkv(mkv_file, output_file)