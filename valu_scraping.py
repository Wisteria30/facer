# -*- coding: utf-8 -*-
import os
import random
import shutil
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# ドライバが設定されるまでの待ち時間を設定する。
driver.implicitly_wait(10)


def category_crawl(path):
    for i in range(28, 29):
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
    # カウント用
    count = 0
    # X-Pathのパス用
    num = 1
    jscroll_added = 0
    while n >= count:
        # 0なら普通のX-PATH それ以外は addedのX-PATHをクリック
        try:
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
            # print("num={}, jscroll_added={}".format(num, jscroll_added))
            # タブの変更
            driver.switch_to.window(driver.window_handles[1])
            # スクショ撮って保存
            take_screenshot()
            # タブの消滅
            driver.close()
            # 元のタブに戻る
            driver.switch_to.window(driver.window_handles[0])
        except:
            num += 1
        # 20越えたらaddedのX-PATHの方へ
        if num >= 20:
            num = 1
            jscroll_added += 1
        else:
            num += 1
        count += 1
    # リンク一つ戻る
    driver.back()


def take_screenshot():
    # スクリーンショット
    icon = driver.find_element_by_class_name("va-img-thumb-cropped__inner")
    jpg = icon.value_of_css_property("background-image")
    jpg = jpg.replace('url("', "").replace('")', "")
    res = requests.get(jpg, stream=True)
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
    filename = "./image/original/" + money + ".jpg"
    if os.path.exists(filename):
        filename = "./image/original/" + money + "__" + str(random.random()) + "__.jpg"
    # 画像を保存
    with open(filename, "wb") as f:
        shutil.copyfileobj(res.raw, f)
        # f.write(jpg)
    # print("export picture {}!!!!!".format(filename))


if __name__ == "__main__":
    # valuのカテゴリページ
    category_crawl("https://valu.is/users/categories/")
