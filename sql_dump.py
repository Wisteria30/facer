import MySQLdb
import re
import urllib.request as urlreq
from bs4 import BeautifulSoup
import requests

# 文字コード(UTF-8)関連
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def make_category_list():
    category_list = []
    # 念のため最大LOOP数を指定しておく
    maxpage = 10000

    # カテゴリーページにアクセス
    for num in range(1,maxpage):
        res = requests.get("https://valu.is/users/categories?page="+str(num))
        soup = BeautifulSoup(res.text, "lxml")

        # Linkの箇所をselect
        links = soup.select(".valuer_category a[href]")

        # もし最終ページだったらforループから抜ける
        if links == []:
            break

        for a in links:
            # Linkタグのhref属性の箇所を抜き出す
            href = a.attrs['href']
            # Link先の最後の数字がカテゴリーナンバー
            hrefOB = re.search(r"\/([0-9]+)",href)
            # カテゴリー名の取得
            vc_name = re.sub("[\t\s\n]+","",a.text)
            vc_name = re.sub("\(.*\)","",vc_name)
            if hrefOB:
                category = [hrefOB.group(1),vc_name]
                category_list.append(category)
    return(category_list)

#各カテゴリーごとにDBへの情報書き込みを実施する
def insert_data(numberOfCat, nameOfCat, cur):
    # 一時的に保存するページのリスト
    # 重複はないと思うけれど重複チェックのために使用
    linkData = []
    # 念のため最大LOOP数を指定しておく
    maxpage = 10000

    # カテゴリーから各IDのリンク先を取得
    for num in range(1,maxpage):
        res = requests.get("https://valu.is/users/categories/"+str(numberOfCat)+"?type=0&page="+str(num))
        soup = BeautifulSoup(res.text, "lxml")

        # Linkの箇所をselect
        links = soup.select(".ranking_info_box a[href]")

        # もし最終ページだったらforループから抜ける
        if links == []:
            break

        for a in links:
            # Linkタグのhref属性の箇所を抜き出す
            href = a.attrs['href']
            # 各IDのリンクを引数に渡してDBへの書き込みを実施する
            if not re.search(r"users",href):
                if not href in linkData:
                    linkData.append(href)
                    insert_data_link(href,nameOfCat,cur)

# Linkから各IDのVALU個別情報を取得してDBに書き込む
def insert_data_link(link,nameOfCat,cur):
    res = requests.get(link+"/data")
    soup = BeautifulSoup(res.text, "lxml")

    # IDはURLから抜き出し
    nameid = re.search(r"https:\/\/valu.is\/(.*)",link).group(1)
    icon_url = re.search(r"url\((.*)\)",str(soup.select_one(".user_icon"))).group(1)
    namestr = re.sub("[\t\s\n]+","",soup.select_one(".user_introduction").text)

    # em tagで順番に 現在値：時価総数：発行VA数：VALUER数となる
    current_value = float(re.sub(",","",soup.select(".news_valu_left em")[0].string))
    ag_market_value = float(re.sub(",","",soup.select(".news_valu_left em")[1].string))
    value_issue = float(re.sub(",","",soup.select(".news_valu_left em")[2].string))
    numerical_value = float(re.sub(",","",soup.select(".news_valu_left em")[3].string))

    data = (nameid,)
    cur.execute("SELECT EXISTS( SELECT * FROM items WHERE id = %s )",data)
    if cur.fetchone()[0]==0:
       # データが存在しない場合には新規で書き込み
       data = (nameid,namestr,icon_url,nameOfCat,current_value,ag_market_value,value_issue,numerical_value)
       cur.execute("INSERT INTO items(id,name,icon,category,current_value,total_value,value_issue,valuer) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",data) 
    else:
       # データが存在する場合には上書き
       data = (namestr,icon_url,nameOfCat,current_value,ag_market_value,value_issue,numerical_value,nameid)
       cur.execute("UPDATE items SET name = %s, icon = %s, category = %s, current_value = %s, total_value = %s, value_issue = %s, valuer = %s \
                    WHERE id = %s",data) 
    cur.execute("COMMIT")

def main():
  conn = MySQLdb.connect(
    user='root',
    passwd='',
    host='localhost',
    db='valu',
    charset="utf8")
  cur = conn.cursor()

  if len(sys.argv) == 2:
    if sys.argv[1] == "init":
    # 初回起動時のみ実施
      print("----- Initialize DB -----")
      cur.execute('DROP TABLE items')
      cur.execute('''
        CREATE TABLE items (
          id TEXT,
          name TEXT,
          icon TEXT,
          category TEXT,
          current_value FLOAT,
          total_value FLOAT,
          value_issue FLOAT,
          valuer FLOAT
        )
      ''')

  # カテゴリーのリストを取得
  category_list = make_category_list()
  for number,name in category_list:
    # Debug用にカテゴリー名は表示する
    print(name)
    insert_data(number,name,cur)

if __name__ == "__main__":
    main()
