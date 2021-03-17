from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),options = options)
driver.get('https://google.com')


import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import csv
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = '高収入'
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", True)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得 iconFont--arrowLeft
    exp_name_list1 = []
    exp_name_list2 = []
    exp_name_list3 = []
    # 検索結果の一番上の会社名を取得
    while True:
        name_list1 = driver.find_elements_by_class_name("cassetteRecruit__name")
        name_list2 = driver.find_elements_by_class_name("tableCondition__head")
        name_list3 = driver.find_elements_by_class_name("tableCondition__body")
        try:
            next_page = driver.find_element_by_class_name("iconFont--arrowLeft")
            next_page.click()
            time.sleep(5)
        except :
            break



    for name1 in name_list1:
        exp_name_list1.append(name1.text)
    for name2 in name_list2:    
        exp_name_list2.append(name2.text)
    for name3 in name_list3:    
        exp_name_list3.append(name3.text)

    d ={"name1":exp_name_list1,"name2":exp_name_list2,"name3":exp_name_list3}

    df = pd.DataFrame.from_dict(d, orient='index').T    

    print(df)

    
    df.to_csv('会社リスト.csv',encoding="cp932")        



    # 1ページ分繰り返し
    
                 


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
     main()
    