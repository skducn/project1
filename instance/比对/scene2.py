# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-9-12
# Description   : 场景2：系统日志行级变更追踪
# 解决思路把新旧日志按行读入，生成带颜色标记的 HTML 差异报告。
# 　　·读入：逐行读取，保留行号与原始顺序。
# 　　· 比对：difflib.HtmlDiff 自动计算增删改。
# 　　· 可视化：直接输出 HTML，浏览器即可查看。
# *********************************************************************


from difflib import HtmlDiff
def generate_log_diff(old_log, new_log, output_file='log_diff.html'):
    """生成可视化日志差异报告"""
    # 仅加载关键错误日志
    def load_key_lines(path):
        with open(path, encoding='utf8') as f:
            # return f.readlines()  # 读取全部日志文件
            # 按需 只提取ERROR级别的日志
            return [line for line in f if 'ERROR' in line or 'WARN' in line]
    # 生成HTML差异报告
    diff = HtmlDiff()
    report = diff.make_file(
        load_key_lines(old_log),
        load_key_lines(new_log),
        fromdesc='旧版本',
        todesc='新版本'
    )
    # 保存报告
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(report)


generate_log_diff(old_log='old.log',new_log='new.log',output_file='diff.html')