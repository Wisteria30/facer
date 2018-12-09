# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
# ドライバが設定されるまでの待ち時間を設定する。
driver.implicitly_wait(10)


for i in range(29):
    # トップ画面を開く
    print("open category {}/28".format(i))
    driver.get("https://valu.is/users/categories/")
    # ローディング待ち
    time.sleep(3)
    # list-count(145) → int: 145
    member_num = driver.find_element_by_xpath(
        '//*[@id="wrap"]/article/div/div[3]/a[{}]/div/span'.format(i + 1)
    ).text
    member_num = member_num.replace("(", "").replace(")", "")
    member_num = int(member_num)
    print(member_num)
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
        print(len(entry_num))
        if len(entry_num) >= member_num - 5:
            break
    # お金を全てリストで取得
    print("--------------------{}------------------------".format(len(entry_num)))
    driver.find_element_by_xpath(
        '//*[@id="wrap"]/article/div/section/div[2]/div/a[1]'
    ).send_keys(Keys.COMMAND, Keys.ENTER)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    # driver.find_element_by_xpath(
    #     '//*[@id="wrap"]/div[8]/div[2]/div[2]/nav/div/ul/li[2]/a'
    # ).click()
    # money = driver.find_element_by_xpath(
    #     '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[2]/section/div/table/tbody/tr[3]/td/span'
    # ).text
    # print(money)
    # driver.back()
    # driver.back()
    # print([money.text for money in moneys])
    driver.back()
print("finish!!!")
# ドライバーを終了
driver.close()


# def member_crawl(n):
#     num = 1
#     jscroll_added = 0
#     while n != num:
#         print("now div{}/div{} // {}".format(jscroll_added, num, n))
#         # 0なら普通のX-PATH それ以外は addedのX-PATHをクリック
#         if not jscroll_added:
#             driver.find_element_by_xpath(
#                 '//*[@id="wrap"]/article/div/section/div[2]/div/a[{}]'.format(num)
#             ).click()
#         else:
#             driver.find_element_by_xpath(
#                 '//*[@id="wrap"]/article/div/section/div[2]/div/div[{}]/div/a[{}]'.format(
#                     jscroll_added, num
#                 )
#             ).click()
#         # スクショ撮って保存
#         take_screenshot()
#         # 20越えたらaddedのX-PATHの方へ
#         if num is 20:
#             num = 1
#             jscroll_added += 1
#         else:
#             num += 1
#     # リンク一つ戻る
#     driver.back()
