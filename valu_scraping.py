# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os
import random

# headlessで使用する場合は以下の2行を利用する。
# options = Options()
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
        # スクロール下までしてリストを全て表示する
        actions = ActionChains(driver)
        scroll_class = driver.find_element_by_class_name("va-footer")
        actions.move_to_element(scroll_class)
        while True:
            actions.perform()
            entry_num = driver.find_elements_by_class_name("va-list-item__info")
            if len(entry_num) >= member_num - 5:
                break
        print(len(entry_num))
        member_crawl(len(entry_num))
    print("finish!!!")
    # ドライバーを終了
    driver.close()
    # driver.quit()


def member_crawl(n):
    num = 1
    jscroll_added = 0
    while n != num:
        # 0なら普通のX-PATH それ以外は addedのX-PATHをクリック
        if jscroll_added is 0:
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/section/div[2]/div/a[{}]'.format(num)
            ).send_keys(Keys.COMMAND, Keys.ENTER)
        else:
            driver.find_element_by_xpath(
                '//*[@id="wrap"]/article/div/section/div[2]/div/div[{}]/div/a[{}]'.format(
                    jscroll_added, num
                )
            ).send_keys(Keys.COMMAND, Keys.ENTER)
        # タブの変更
        driver.switch_to.window(driver.window_handles[1])
        # スクショ撮って保存
        take_screenshot()
        # タブの消滅
        driver.close()
        # 元のタブに戻る
        driver.switch_to.window(driver.window_handles[0])
        # 20越えたらaddedのX-PATHの方へ
        if num is 20:
            num = 1
            jscroll_added += 1
        else:
            num += 1
    # リンク一つ戻る
    driver.back()


def take_screenshot():
    # スクリーンショット
    png = driver.find_element_by_class_name(
        "va-img-thumb-cropped__inner"
    ).screenshot_as_png
    # お金の金額を取る
    driver.find_element_by_link_text("データ").click()
    try:
        money = driver.find_element_by_xpath(
            '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[2]/section/div/table/tbody/tr[3]/td/span'
        ).text
    except:
        money = driver.find_element_by_xpath(
            '//*[@id="wrap"]/div[2]/div[3]/div[2]/div[2]/section/div/table/tbody/tr[3]/td/span'
        ).text
    money = money.replace("BTC", "")
    driver.back()
    # 同一ファイル名が存在するか確認
    filename = "./img/" + money + ".png"
    if os.path.exists(filename):
        filename = "./img/" + money + "__" + str(random.random()) + ".png"
    # 画像を保存
    with open(filename, "wb") as f:
        f.write(png)
    print("export picture ./img/{}.png!!!!!".format(filename))


if __name__ == "__main__":
    # valuのカテゴリページ
    category_crawl("https://valu.is/users/categories/")
