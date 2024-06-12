import time
import requests
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class TgdCrawler:
    """
    Crawl posts, content, and response from tgd.kr
    """
    def __init__(self):
        self.options = Options()
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        self.base_url = "https://tgd.kr/s/miacat1009"
        self.posts_csv = "tgd-crawler/tgd.csv"
        self.backup_folder = "tgd-crawler/backup"

        self.sleeping_time = random.randint(3, 6)

    def crawl_posts(self, start_page=1, end_page=103, start_row=4, end_row=32):
        """
        Crawl posts from tgd.kr
        :param start_page: int, start page number
        :param end_page: int, end page number
        :param start_row: int, start row number
        :param end_row: int, end row number
        :return: None
        """
        for page in range(start_page, end_page):
            url = f'https://tgd.kr/s/miacat1009/page/{page}'
            self.driver.get(url)
            time.sleep(self.sleeping_time)

            for row in range(start_row, end_row + 1):
                if (page == 1) and (row < 7):
                    continue
                if (page != 1) and (row > 32):
                    continue

                category = f'/html/body/div[2]/div/div/div[2]/div/div[2]/div[{row}]/div/div[2]/div[1]/span'
                title = f'/html/body/div[2]/div/div/div[2]/div/div[2]/div[{row}]/div/div[2]/a'
                author = f'/html/body/div[2]/div/div/div[2]/div/div[2]/div[{row}]/div/div[2]/div[2]/span'
                date = f'/html/body/div[2]/div/div/div[2]/div/div[2]/div[{row}]/div/div[3]'

                category_text = self.driver.find_element(By.XPATH, category).text
                title_text = self.driver.find_element(By.XPATH, title).text
                content_link = self.driver.find_element(By.XPATH, title).get_attribute("href")
                author_text = self.driver.find_element(By.XPATH, author).text
                date_text = self.driver.find_element(By.XPATH, date).text

                with open(self.posts_csv, mode='a', newline='', encoding='utf8') as file:
                    writer = csv.writer(file)
                    writer.writerow([page, row, category_text, title_text, content_link, author_text, date_text])

                if page == 1:
                    print(f'page: {page} / 102\n row: {row - 3} / 33')
                else:
                    print(f'page: {page} / 102\n row: {row - 3} / 29')

                if (page == 102) and (row == 32):
                    break

    def crawl_content(self):
        """
        Crawl content from tgd.kr
        :return: None
        """
        with open(self.posts_csv, mode='r', encoding='utf8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            max_length = len(rows)
            for row in rows:
                content_link = row[4]

                self.driver.get(content_link)
                time.sleep(self.sleeping_time)

                CONTENT = '/html/body/div[2]/div/div/div[2]/div/div[4]/div[2]'
                content_txt = self.driver.find_element(By.XPATH, CONTENT).text
                file_name = content_link.split('/')[-1]

                with open(f'{self.backup_folder}/content-{file_name}.txt', 'w', encoding='utf8') as file:
                    file.write(content_txt)

                print(f"Progress: {rows.index(row) + 1}/{max_length}")

    def crawl_response(self):
        """
        Crawl response from tgd.kr
        :return: None
        """
        with open(self.posts_csv, mode='r', encoding='utf8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            max_length = len(rows)

            for row in rows:
                content_link = row[4]
                response = requests.get(content_link)
                content = response.text

                file_name = content_link
                with open(f"{self.backup_folder}/response-{file_name}.txt", "w") as file:
                    file.write(content)

                print(f"Progress: {rows.index(row) + 1}/{max_length}")

    def crawl_html(self):
        with open(self.posts_csv, mode='r', encoding='utf8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            max_length = len(rows)
            for row in rows:
                content_link = row[4]

                self.driver.get(content_link)
                time.sleep(self.sleeping_time)

                content_box = '/html/body/div[2]/div/div/div[2]/div/div[4]/div[2]'
                element = self.driver.find_element(By.XPATH, content_box)
                html = element.get_attribute('innerHTML')

                file_name = content_link.split('/')[-1]
                with open(f"{self.backup_folder}/html-{file_name}.html", "w", encoding='utf8') as file:
                    file.write(html)

    def crawl_images(self):
        """
        Crawl images from tgd.kr
        :return: None
        """
        with open(self.posts_csv, mode='r', encoding='utf8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            max_length = len(rows)

            for row in rows:
                content_link = row[4]
                self.driver.get(content_link)
                time.sleep(self.sleeping_time)

                IMAGES = '/html/body/div[2]/div/div/div[2]/div/div[4]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div'

                break

    def close(self):
        """
        Close the driver
        :return: None
        """
        self.driver.quit()

crawler = TgdCrawler()
crawler.crawl_html()
crawler.close()
