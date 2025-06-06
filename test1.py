

import pyttsx3,os



def text_to_speech(text, output_file='output.mp3', rate=200, volume=1.0, voice_id=None):
    """
    将文字转换为语音并保存为音频文件

    参数:
    - text: 要转换的文本
    - output_file: 输出音频文件路径
    - rate: 语速（默认200）
    - volume: 音量（0.0到1.0，默认1.0）
    - voice_id: 语音ID（默认使用系统默认语音）
    """
    # 初始化引擎
    engine = pyttsx3.init()

    # 设置语速
    engine.setProperty('rate', rate)

    # 设置音量
    engine.setProperty('volume', volume)

    # 设置语音（可选）
    if voice_id:
        engine.setProperty('voice', voice_id)

    # 保存为文件
    engine.save_to_file(text, output_file)

    # 运行引擎并等待完成
    engine.runAndWait()

    print(f"语音已保存到: {output_file}")


# 使用示例
text = "你好，这是一个文字转语音的示例。"
text_to_speech(text, "hello.mp3")