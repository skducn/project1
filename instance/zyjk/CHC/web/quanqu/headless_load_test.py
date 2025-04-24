import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PO.WebPO import *
Web_PO = WebPO("chromeCookies")


def test_url(url):
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options=chrome_options)

    try:
        start_time = time.time()
        Web_PO.openUrlByCookies('http://192.168.0.243:8010/', 'http://192.168.0.243:8010/#/SignManage/signAssess',
                                'cookies.json')

        # driver.get(url)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"访问 {url} 的响应时间: {response_time:.2f} 秒")
        return response_time
    except Exception as e:
        print(f"访问 {url} 时出错: {e}")
        return None
    finally:
        Web_PO.quit()
        # driver.quit()


def perform_load_test(url, num_users, num_requests_per_user):
    total_response_times = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = []
        for _ in range(num_users):
            for _ in range(num_requests_per_user):
                future = executor.submit(test_url, url)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            response_time = future.result()
            if response_time is not None:
                total_response_times.append(response_time)

    if total_response_times:
        average_response_time = sum(total_response_times) / len(total_response_times)
        print(f"平均响应时间: {average_response_time:.2f} 秒")
    else:
        print("未收集到有效的响应时间数据。")


if __name__ == "__main__":
    target_url = "http://192.168.0.243:8010/#/SignManage/service"  # 替换为你要测试的URL
    num_concurrent_users = 10  # 并发用户数
    num_requests_per_user = 5  # 每个用户的请求次数

    perform_load_test(target_url, num_concurrent_users, num_requests_per_user)
