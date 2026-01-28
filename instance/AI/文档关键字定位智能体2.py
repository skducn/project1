# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-26
# Description: 该智能体核心实现本地文件 / 表格解析 + 关键字精准 / 模糊检索 + 内容定位展示，支持主流文档格式（TXT/MD/Excel/Csv/PDF/Word），适配 Windows/Mac 跨平台，采用 Python 开发（契合技术栈），兼具轻量性、易用性和可扩展性，可直接本地部署运行，无需依赖云端服务。
# 路径输入：支持绝对路径，输入时可去掉首尾的引号（代码已做兼容）；
# 文件夹检索：会递归解析文件夹下所有子文件夹的支持格式文件；
# 组合检索：直接输入关键字1&关键字2（同时包含）或关键字1|关键字2（包含其一）；
# 跨平台：Windows/Mac 均适用，Mac 获取文件 / 文件夹绝对路径可右键「显示简介」，Windows 可按住 Shift 右键「复制为路径」。
# *****************************************************************

import gradio as gr
from doc_search_agent import DocSearchAgent
import os

agent = DocSearchAgent()


def search_docs(file, files, folder_path, keywords, search_mode):
    agent.file_parsed_data.clear()

    if file:
        # 单个文件处理
        agent.parse_file(file.name)
    elif files:
        # 多文件处理
        for uploaded_file in files:
            agent.parse_file(uploaded_file.name)
    elif folder_path and os.path.isdir(folder_path):
        # 文件夹路径处理
        agent.parse_folder(folder_path)
    else:
        return "请上传文件、选择多个文件或输入文件夹路径！"

    # 直接返回完整的搜索结果
    result = agent.search(keywords, search_mode)
    return result


with gr.Blocks() as demo:
    gr.Markdown("# 文档关键字定位智能体")
    with gr.Row():
        file = gr.File(label="上传单个文件")
        files = gr.Files(label="上传多个文件")
        folder_path = gr.Textbox(label="输入文件夹路径", placeholder="例：/path/to/folder")
    keywords = gr.Textbox(label="输入检索关键字", placeholder="例：黄金&5000美元 或 黄金|白银")
    search_mode = gr.Dropdown(["精准", "模糊", "组合"], label="检索模式", value="模糊")
    btn = gr.Button("开始检索")
    output = gr.Textbox(label="检索结果", interactive=False, lines=20, max_lines=50)
    btn.click(search_docs, [file, files, folder_path, keywords, search_mode], output)

demo.launch()
