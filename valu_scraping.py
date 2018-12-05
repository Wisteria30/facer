# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# options = Options()
# headlessで使用する場合は以下の2行を利用する。
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
# ドライバが設定されるまでの待ち時間を設定する。
driver.implicitly_wait(10)


def category_crawl(path):
    for i in range(29):
        # トップ画面を開く
        print("open category {}/28".format(i))
        driver.get(path)
        # ローディング待ち
        time.sleep(3)
        # list-count(145) → int: 145
        member_num = driver.find_element_by_xpath(
            '//*[@id="wrap"]/article/div/div[3]/a[{}]/div/span'.format(i + 1)
        ).text
        member_num = member_num.replace("(", "").replace(")", "")
        member_num = int(member_num)
        # 上のカテゴリーから順に入っていく
        driver.find_element_by_xpath(
            '//*[@id="wrap"]/article/div/div[3]/a[{}]'.format(i + 1)
        ).click()
        member_crawl(member_num)
    print("finish!!!")
    # ドライバーを終了
    driver.close()
    # driver.quit()


def member_crawl(n):
    num = 1
    jscroll_added = 0
    while n != num:
        print("now div{}/div{} // {}".format(jscroll_added, num, n))
        # 0なら普通のX-PATH それ以外は addedのX-PATHをクリック
        if jscroll_added is 0:
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/section/div[2]/div/a[{}]'.format(num)
            ).click()
        else:
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/section/div[2]/div/div[{}]/div/a[{}]'.format(
                    jscroll_added, num
                )
            ).click()
        # スクショ撮って保存
        take_screenshot()
        # 20越えたらaddedのX-PATHの方へ
        if num is 20:
            num = 1
            jscroll_added += 1
        else:
            num += 1
    # リンク一つ戻る
    driver.back()


def take_screenshot():
    # スクショ
    png = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[8]/div[2]/div[2]/div[1]/section[1]/div/div/span/span'
    ).screenshot_as_png
    # お金の金額を取る
    driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[8]/div[2]/div[2]/nav/div/ul/li[2]/a'
    ).click()
    money = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[2]/section/div/table/tbody/tr[3]/td/span'
    ).text
    money = money.replace("BTC", "")
    driver.back()
    # 画像を保存
    with open("./img/" + money + ".png", "wb") as f:
        f.write(png)
    print("export picture ./img/{}.png!!!!!".format(money))
    # リンク一つ戻る
    driver.back()


# valuのカテゴリページ
category_crawl("https://valu.is/users/categories/")
