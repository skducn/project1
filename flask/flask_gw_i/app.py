from flask import Flask, send_from_directory
import os
app = Flask(__name__)
# Allure 报告生成的目录
ALLURE_REPORT_DIR = 'allureReport'

@app.route('/')
def index():
    return send_from_directory(ALLURE_REPORT_DIR, 'index.html')

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory(ALLURE_REPORT_DIR, path)


if __name__ == '__main__':
    # 确保 Allure 报告目录存在
    if not os.path.exists(ALLURE_REPORT_DIR):
        print(f"Allure 报告目录 {ALLURE_REPORT_DIR} 不存在，请先生成 Allure 报告。")
    else:
        app.run(debug=True)
