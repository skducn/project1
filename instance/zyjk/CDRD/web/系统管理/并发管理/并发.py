# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2026-2-27
# Description: 同时执行新增角色和编辑角色脚本（调用原脚本版本）
# 功能：在异步环境中调用原有的同步Playwright脚本
# *****************************************************************

import os
import sys
import asyncio
import subprocess
from datetime import datetime
from playwright.async_api import async_playwright

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


async def run_script_in_subprocess(script_name, tab_name):
    """在子进程中运行指定的脚本"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 开始执行 {tab_name}")

        script_path = os.path.join(current_dir, f"{script_name}.py")

        # 使用subprocess运行脚本
        process = await asyncio.create_subprocess_exec(
            sys.executable, script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 等待进程完成
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {tab_name} 执行完成")
            if stdout:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 {tab_name} 输出: {stdout.decode('utf-8').strip()}")
            return {"status": "success", "output": stdout.decode('utf-8') if stdout else ""}
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {tab_name} 执行失败")
            if stderr:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {tab_name} 错误: {stderr.decode('utf-8').strip()}")
            return {"status": "failed", "error": stderr.decode('utf-8') if stderr else "Unknown error"}

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {tab_name} 执行出错: {str(e)}")
        return {"status": "error", "message": str(e)}


async def execute_original_scripts():
    """执行原始脚本文件"""
    print("=" * 60)
    print("【原始脚本并行执行】开始同时执行新增角色和编辑角色脚本")
    print("=" * 60)

    # 记录开始时间
    start_time = datetime.now()
    print(f"[{start_time.strftime('%H:%M:%S')}] ⏱️ 开始并行执行...")

    # 同时执行两个脚本
    task1 = asyncio.create_task(run_script_in_subprocess("新增角色", "新增角色"))
    task2 = asyncio.create_task(run_script_in_subprocess("编辑角色", "编辑角色"))

    # 等待两个任务完成
    result1 = await task1
    result2 = await task2

    # 记录结束时间
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    print(f"[{end_time.strftime('%H:%M:%S')}] 🎉 所有脚本执行完成")
    print(f"⏱️ 总执行时间: {duration} 秒")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 新增角色结果: {result1}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 编辑角色结果: {result2}")

    print("=" * 60)
    print("【原始脚本并行执行】全部完成")
    print("=" * 60)



# 如果直接运行此脚本
if __name__ == "__main__":
    # 使用子进程方式（最稳定）
    asyncio.run(execute_original_scripts())
