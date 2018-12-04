# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
# headlessで使用する場合は以下の2行を利用する。
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)
# ドライバが設定されるまでの待ち時間を設定する。
driver.implicitly_wait(10)
# valuのカテゴリページ
path = "https://valu.is/users/categories/"


def category_crawl():
    for i in range(29):
        # トップ画面を開く
        driver.get(path + str(i))
        # ローディング待ち
        time.sleep(3)
        # list-count(145) → int: 145
        member_num = int(
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/div[3]/a[{}]/div/span'.format(i + 1)
            )
            .text.split(")", "")
            .split("(", "")
        )
        # 上のカテゴリーから順に入っていく
        driver.find_element_by_xpath(
            '//*[@id="wrap"]/article/div/div[3]/a[{}]'.format(i + 1)
        ).click()
        scraping(member_num)


def scraping(n):
    jscroll_added = n // 20
    num = 1
    while n != num:
        while num <= 20:
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/section/div[2]/div/a[{}]'.format(num)
            ).click()
            take_screenshot()
            driver.back()
            num += 1
        for k in range(jscroll_added):
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/section/div[2]/div/div[{}]/div/a[{}]'.format(
                    k + 1, num
                )
            ).click()
            take_screenshot()
            driver.back()
            num = 1 if num is 20 else num + 1


def take_screenshot():
    png = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[8]/div[2]/div[2]/div[1]/section[1]/div/div/span/span'
    ).screenshot_as_png
    money = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[8]/div[2]/div[2]/div[1]/section[2]/div/table/tbody[2]/tr/td/span'
    ).text
    print(money)
    # 画像を保存
    with open("./img/" + money, "wb") as f:
        f.write(png)


# ドライバーを終了
driver.close()
# driver.quit()
