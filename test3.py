import argparse
import os
import ssl
import tempfile

import whisper
from moviepy.editor import VideoFileClip

ssl._create_default_https_context = ssl._create_unverified_context

#  python test3.py /Users/linghuchong/Desktop/400.mp4 -o test33.srt
# pip install moviepy==1.0.3  # 稳定版本
# /Applications/Python\ 3.9/Install\ Certificates.command


def extract_audio(video_path, audio_output_path):
    """从视频中提取音频"""
    print(f"正在从视频中提取音频: {video_path}")
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_output_path)
        audio.close()
        video.close()
        print(f"音频已提取到: {audio_output_path}")
        return True
    except Exception as e:
        print(f"提取音频时出错: {e}")
        return False


def speech_to_text(audio_path, model_size="small", output_path=None):
    """将音频转换为文本"""
    print(f"正在加载 Whisper 模型: {model_size}")
    model = whisper.load_model(model_size)
    # model = whisper.load_model("./models/small/")

    print(f"正在识别音频: {audio_path}")
    result = model.transcribe(audio_path)

    text = result["text"]

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"文本已保存到: {output_path}")

    return text


def main():
    parser = argparse.ArgumentParser(description="视频语音转文字工具")
    parser.add_argument("video_path", help="视频文件路径")
    parser.add_argument("-o", "--output", help="输出文本文件路径")
    parser.add_argument(
        "-m",
        "--model",
        help="Whisper 模型大小 (tiny, base, small, medium, large)",
        default="small",
    )
    parser.add_argument("--keep-audio", action="store_true", help="保留临时音频文件")

    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        print(f"错误: 视频文件不存在: {args.video_path}")
        return

    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "temp_audio.wav")

    try:
        # 提取音频
        if not extract_audio(args.video_path, audio_path):
            return

        # 语音转文字
        output_path = args.output or os.path.splitext(args.video_path)[0] + ".txt"
        text = speech_to_text(audio_path, args.model, output_path)

        print("\n转换结果预览:")
        print(text[:300] + ("..." if len(text) > 300 else ""))

    finally:
        # 清理临时文件
        if os.path.exists(audio_path) and not args.keep_audio:
            os.remove(audio_path)
        os.rmdir(temp_dir)


if __name__ == "__main__":
    main()
