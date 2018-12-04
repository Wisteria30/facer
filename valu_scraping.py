# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
# chromeのパスを指定する。今回は環境変数から取得

# headlessで使用する場合は以下の2行を利用する。
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# webdriverを起動する。引数executable_pathにwebdriverのパスを指定する。
# こちらも環境変数から取得
driver = webdriver.Chrome(options=options)

# ドライバが設定されるまでの待ち時間を設定する。
driver.implicitly_wait(10)

# トップ画面を開く。
driver.get("https://valu.is/takapon")

# ローディング待ち
time.sleep(3)

# タイトル部分の画像オブジェクトを取得する。
assert "VALU" in driver.title
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
