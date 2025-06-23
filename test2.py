import os
import argparse
import tempfile
import subprocess
import re
from datetime import timedelta
import cv2
import pytesseract
from pytesseract import Output


# 设置 Tesseract OCR 路径（根据你的安装路径调整）
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Linux/Mac
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows

def extract_hard_subtitles(video_path, language='eng', frames_per_second=1):
    """从视频画面中提取硬字幕"""
    print("开始提取硬字幕...")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"错误：无法打开视频文件 {video_path}")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps / frames_per_second))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"视频信息：FPS={fps:.2f}, 总帧数={total_frames}, 时长={timedelta(seconds=duration)}")
    print(f"将每 {frame_interval} 帧提取一次，约 {frames_per_second} 帧/秒")

    subtitles = []
    prev_text = ""
    frame_count = 0
    processed_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # 计算当前时间
            time_stamp = frame_count / fps
            minutes, seconds = divmod(time_stamp, 60)
            hours, minutes = divmod(minutes, 60)
            time_code = f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"

            # 转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 使用 OCR 识别文本
            data = pytesseract.image_to_data(gray, lang=language, output_type=Output.DICT)
            text = " ".join([word for word in data['text'] if word.strip()])

            # 过滤空文本和重复文本
            if text.strip() and text != prev_text:
                subtitles.append({
                    'start_time': time_code,
                    'text': text
                })
                prev_text = text
                print(f"已处理 {processed_frames} 帧，识别到字幕: {text[:50]}...")

            processed_frames += 1

        frame_count += 1

    cap.release()

    # 为字幕添加结束时间
    for i in range(len(subtitles) - 1):
        subtitles[i]['end_time'] = subtitles[i + 1]['start_time']

    if subtitles:
        subtitles[-1]['end_time'] = str(timedelta(seconds=duration))

    print(f"硬字幕提取完成，共识别出 {len(subtitles)} 条字幕")
    return subtitles


def extract_soft_subtitles(video_path):
    """从视频中提取软字幕轨道"""
    print("开始提取软字幕...")
    temp_dir = tempfile.mkdtemp()
    subtitles = []

    try:
        # 使用 ffprobe 检测字幕轨道
        probe_cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 's',
            '-show_entries', 'stream=index,codec_name,title',
            '-of', 'csv=p=0',
            video_path
        ]

        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：无法检测字幕轨道 - {result.stderr}")
            return []

        # 解析字幕轨道信息
        tracks = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(',')
                track_info = {
                    'index': parts[0],
                    'codec': parts[1] if len(parts) > 1 else 'unknown',
                    'title': parts[2] if len(parts) > 2 else ''
                }
                tracks.append(track_info)

        if not tracks:
            print("未检测到软字幕轨道")
            return []

        print(f"检测到 {len(tracks)} 条字幕轨道")
        for i, track in enumerate(tracks):
            print(f"{i + 1}. 索引: {track['index']}, 编码: {track['codec']}, 标题: {track['title']}")

        # 默认提取第一条字幕轨道
        selected_track = tracks[0]
        print(f"选择提取字幕轨道 {selected_track['index']}")

        # 提取字幕文件
        subtitle_file = os.path.join(temp_dir, f"subtitles_{selected_track['index']}.srt")
        extract_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-map', f'0:{selected_track["index"]}',
            '-c', 'copy',
            subtitle_file
        ]

        result = subprocess.run(extract_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：无法提取字幕 - {result.stderr}")
            return []

        if os.path.exists(subtitle_file):
            # 读取并解析 SRT 文件
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                srt_content = f.read()

            subtitles = parse_srt(srt_content)
            print(f"软字幕提取完成，共 {len(subtitles)} 条字幕")

    finally:
        # 清理临时文件
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

    return subtitles


def parse_srt(srt_content):
    """解析 SRT 格式字幕"""
    subtitles = []
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?:\n\n|$)')

    for match in pattern.finditer(srt_content):
        index = match.group(1)
        start_time = match.group(2).replace(',', '.')
        end_time = match.group(3).replace(',', '.')
        text = match.group(4).strip()

        subtitles.append({
            'index': index,
            'start_time': start_time,
            'end_time': end_time,
            'text': text
        })

    return subtitles


def save_subtitles(subtitles, output_file, format='srt'):
    """保存字幕到文件"""
    if not subtitles:
        print("没有字幕内容可保存")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        if format.lower() == 'srt':
            for i, subtitle in enumerate(subtitles, 1):
                # f.write(f"{i}\n")
                # f.write(f"{subtitle['start_time'].replace('.', ',')} --> {subtitle['end_time'].replace('.', ',')}\n")
                f.write(f"{subtitle['text']}\n\n")
        elif format.lower() == 'txt':
            for subtitle in subtitles:
                f.write(f"[{subtitle['start_time']}] {subtitle['text']}\n")

    print(f"字幕已保存到 {output_file}")


def main():
    parser = argparse.ArgumentParser(description='视频字幕提取工具')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径', default='subtitles.srt')
    parser.add_argument('-l', '--language', help='OCR 语言代码 (用于硬字幕)', default='eng')
    parser.add_argument('-f', '--fps', type=int, help='提取硬字幕时的每秒帧数', default=1)
    parser.add_argument('--only-hard', action='store_true', help='只提取硬字幕')
    parser.add_argument('--only-soft', action='store_true', help='只提取软字幕')

    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        print(f"错误：视频文件 {args.video_path} 不存在")
        return

    subtitles = []

    # 优先提取软字幕
    if not args.only_hard:
        subtitles = extract_soft_subtitles(args.video_path)

    # 如果没有软字幕或者指定了提取硬字幕
    if (not subtitles or args.only_hard) and not args.only_soft:
        subtitles = extract_hard_subtitles(args.video_path, args.language, args.fps)

    if subtitles:
        output_format = args.output.split('.')[-1] if '.' in args.output else 'srt'
        save_subtitles(subtitles, args.output, output_format)
    else:
        print("未找到任何字幕")


if __name__ == "__main__":
    main()


    #    python test2.py /Users/linghuchong/Desktop/400.mp4 -o subtitles1.srt --only-hard
    #    python test2.py /Users/linghuchong/Desktop/400.mp4 -o output.srt -l chi_sim --only-hard