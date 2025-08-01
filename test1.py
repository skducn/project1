import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import logging
from urllib.parse import urljoin

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HospitalCrawler:
    def __init__(self):
        self.base_url = "http://zgcx.nhc.gov.cn:9090"
        self.search_url = urljoin(self.base_url, "/unit/index")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.base_url,
            "Referer": self.search_url
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.total_pages = 1  # 初始化总页数
        self.current_page = 1  # 当前页码
        self.results = []  # 存储结果
        self.output_file = "hospitals.csv"  # 输出文件名

    def get_total_pages(self):
        """获取总页数"""
        try:
            # 先发送一个请求获取总页数
            data = {
                "p": "1",
                "pSize": "10",
                "legalPerson": "",
                "areaCode": "",
                "orgName": "",
                "orgLevel": "",
                "orgClassify": "",
                "orgProperty": "",
                "isSocial办医": ""
            }
            response = self.session.post(self.search_url, data=data)
            response.raise_for_status()

            # 解析总页数
            soup = BeautifulSoup(response.text, 'html.parser')
            total_pages_elem = soup.select_one('.pagination li:nth-last-child(2) a')
            if total_pages_elem:
                self.total_pages = int(total_pages_elem.text.strip())
                logger.info(f"总页数: {self.total_pages}")
            else:
                logger.warning("无法获取总页数，将按单页处理")
                self.total_pages = 1

        except Exception as e:
            logger.error(f"获取总页数失败: {e}")
            self.total_pages = 1

    def parse_page(self, page_num):
        """解析单页数据"""
        try:
            data = {
                "p": str(page_num),
                "pSize": "10",  # 每页10条数据
                "legalPerson": "",
                "areaCode": "",
                "orgName": "",
                "orgLevel": "",
                "orgClassify": "",
                "orgProperty": "",
                "isSocial办医": ""
            }

            response = self.session.post(self.search_url, data=data)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('.table.table-hover')

            if not table:
                logger.warning(f"第 {page_num} 页未找到数据表格")
                return

            rows = table.select('tbody tr')
            for row in rows:
                cols = row.select('td')
                if len(cols) >= 4:
                    hospital = {
                        'name': cols[0].text.strip(),
                        'code': cols[1].text.strip(),
                        'level': cols[2].text.strip(),
                        'address': cols[3].text.strip()
                    }
                    self.results.append(hospital)
                    logger.info(f"已抓取: {hospital['name']} - {hospital['code']}")

            logger.info(f"第 {page_num} 页抓取完成，共 {len(rows)} 条记录")

        except Exception as e:
            logger.error(f"解析第 {page_num} 页失败: {e}")

    def save_to_csv(self):
        """保存结果到CSV文件"""
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['name', 'code', 'level', 'address']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
            logger.info(f"数据已保存到 {self.output_file}，共 {len(self.results)} 条记录")
        except Exception as e:
            logger.error(f"保存CSV文件失败: {e}")

    def run(self):
        """运行爬虫"""
        try:
            logger.info("开始爬取全国医疗机构数据...")
            self.get_total_pages()

            # 爬取每一页数据
            for page in range(1, self.total_pages + 1):
                self.current_page = page
                self.parse_page(page)

                # 随机延时，避免过快请求
                delay = random.uniform(1, 3)
                logger.info(f"等待 {delay:.2f} 秒后继续...")
                time.sleep(delay)

            # 保存结果
            self.save_to_csv()
            logger.info("爬取完成！")

        except KeyboardInterrupt:
            logger.info("用户中断，保存已抓取数据...")
            self.save_to_csv()
        except Exception as e:
            logger.error(f"爬取过程中发生错误: {e}")
            self.save_to_csv()


if __name__ == "__main__":
    crawler = HospitalCrawler()
    crawler.run()    