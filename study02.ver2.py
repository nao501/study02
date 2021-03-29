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
import logging



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
    return Chrome(ChromeDriverManager().install(), options=options)
# main処理
def main():
    search_keyword = input('キーワードを入力してください：')
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
    
    #ログの出力

    formatter = '%(asctime)s[%(filename)s:%(lineno)d　%(levelname)s]'
    logging.basicConfig(filename='debug.py',level = logging.DEBUG,format=formatter)
    logging.critical('クリティカル')
    logging.error('エラー')
    logging.warning('警告')
    logging.debug(('デバッグ'))
    logging.info('%s %s', 'test', 'test')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_file = logging.FileHandler('debug.py')
    logger.addHandler(log_file)

    logger.debug('debugメッセージ')

    # 取得したデータを収納するリスト
    exp_name_list1 = []
    exp_name_list2 = []
    exp_name_list3 = []
    driver.implicitly_wait(5)

    #ページカウント用
    count = 1
    
    while True : #無限ループにしてページ切り替え部分でbreak判定する
        name_list1 = driver.find_elements_by_class_name("cassetteRecruit__name")
        name_list2 = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition tr:nth-child(1) .tableCondition__head") # 広告が混じらないように.cassettreRecruitを付与する
        name_list3 = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition tr:nth-child(1) .tableCondition__body")
        for name1 in name_list1:
         exp_name_list1.append(name1.text)
        for name2 in name_list2:    
         exp_name_list2.append(name2.text)
        for name3 in name_list3:    
         exp_name_list3.append(name3.text)
        driver.implicitly_wait(10)
        print(str(count) + 'ページ目のデータを取得しました')
        
        try:
            count += 1
            next_page_elm = driver.find_element_by_class_name("iconFont--arrowLeft")
            url = next_page_elm.get_attribute("href")
            driver.get(url)
        except:
            print("\n\n最後のページの処理が終わりました\n\n")
            break

    d ={"name1":exp_name_list1,"name2":exp_name_list2,"name3":exp_name_list3}
    df = pd.DataFrame(d)
    df.to_csv('会社リスト.csv',encoding="utf-8_sig") #utf8-sigの方がExcelで開けて汎用的
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
     main()