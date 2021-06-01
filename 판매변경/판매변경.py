# coding: utf-8

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
import numpy as np
import pandas as pd


print()
print("이 프로그램은 김연혁 이 제작한 프로그램입니다.")
print()
account_id = input("네이버 아이디를 입력해주세요: ")
account_password = input("네이버 비밀번호를 입력해주세요: ")
print()


# xpath에 해당하는 element를 클릭하고 원하는 만큼 대기하는 함수
def element_click(driver, xpath, sleep):
    driver.find_element_by_xpath(xpath).click()
    time.sleep(sleep)


# xpath에 해당하는 element에 원하는 문자열을 send하는 함수
def element_send_keys(driver, xpath, string):
    element = driver.find_element_by_xpath(xpath)
    element.send_keys(string)


def login():
    now_dir = os.getcwd()

    # 크롤링한 웹사이트 포털
    link = 'https://sell.smartstore.naver.com/#/products/navershopping-match-product'
    # chromedriver의 경로 설정
    path = "chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument('--start-fullscreen')
    options.add_experimental_option("prefs", {
        "download.default_directory": now_dir,
        "download.prompt_for_download": False,
        "donwload.directory_updrade": True
    })

    try:
        driver = webdriver.Chrome(path, options=options)
    except:
        print("Chrome driver의 파일 경로를 확인하거나 버전을 체크해 주시기 바랍니다.")

    driver.get(link)
    time.sleep(1.5)

    element_click(driver, """/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a""", 1.0)

    element_send_keys(driver, """//*[@id="id"]""", account_id)
    element_send_keys(driver, """//*[@id="pw"]""", account_password)
    element_click(driver, """//*[@id="log.login"]""", 0)

    element = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""")))
    element.click()

    try:
        WebDriverWait(driver, 1.0).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a"""))).click()
    except:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a"""))).click()
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a"""))).click()

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                                        """//*[@id="seller-content"]/div[2]/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button"""))).click()
    except:
        time.sleep(0.5)

    time.sleep(2)

    return driver


def relogin(driver):
    driver.close()

    now_dir = os.getcwd()

    # 크롤링한 웹사이트 포털
    link = 'https://sell.smartstore.naver.com/#/products/navershopping-match-product'
    # chromedriver의 경로 설정
    path = "chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": now_dir,
        "download.prompt_for_download": False,
        "donwload.directory_updrade": True
    })

    try:
        driver = webdriver.Chrome(path, options=options)
    except:
        print("Chrome driver의 파일 경로를 확인하거나 버전을 체크해 주시기 바랍니다.")

    driver.get(link)
    time.sleep(1.5)

    # 네이버 로그인 선택
    element_click(driver, """/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a""", 1.0)

    # 아이디 비밀번호 넣고 로그인
    element_send_keys(driver, """//*[@id="id"]""", account_id)
    element_send_keys(driver, """//*[@id="pw"]""", account_password)
    element_click(driver, """//*[@id="log.login"]""", 0)

    element = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""")))
    element.click()

    try:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)
    except:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                                    """//*[@id="seller-content"]/div[2]/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button"""))).clicl()
    except:
        time.sleep(0.5)


def data_collect(driver):
    # 판매중 버튼 없애기
    driver.find_element_by_xpath(
        """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[2]/div/div/div/label[3]""").click()
    time.sleep(0.1)
    # 판매중지 버튼 클릭
    driver.find_element_by_xpath(
        """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[2]/div/div/div/label[6]""").click()
    time.sleep(0.1)

    # 1년
    driver.find_element_by_xpath(
        """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[6]/div/div/ncp-datetime-range-picker2/div[1]/div/div/button[6]""").click()
    time.sleep(0.1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3)")
    time.sleep(0.3)

    driver.find_element_by_xpath(
        """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""").click()  # 검색
    time.sleep(1.0)

    # 전체 항목 엑셀파일 저장
    driver.find_element_by_xpath(
        """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[1]/div[2]/div/div[2]/button""").click()
    time.sleep(0.5)

    while True:
        try:
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        except:
            time.sleep(0.5)
        else:
            break

    time.sleep(1.0)

    while True:
        file_list = os.listdir('./')
        file_list = [file for file in file_list if file.endswith(".csv")]

        if len(file_list) == 1:
            break
        else:
            time.sleep(0.3)

    product_csv = pd.read_csv(file_list[0])
    os.remove(file_list[0])

    pro_codes = list()

    for i in range(len(product_csv)):
        pro = product_csv.iloc[i]
        pro_codes.append(str(pro[0]))

    return pro_codes


def change(driver, codes):
    i = 0

    for pro_code in codes:
        # 상품번호 입력
        textarea = driver.find_element_by_xpath(
            """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea""")
        textarea.clear()
        textarea.send_keys(pro_code)
        time.sleep(0.5)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                                            """//*[@id="seller-content"]/div[2]/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button"""))).click()
        except:
            time.sleep(0.5)

        driver.find_element_by_xpath(
            """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[2]/div/div/div/label[1]/span""").click()

        # 검색
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""")))
        element.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")
        time.sleep(0.3)

        # 수정 버튼 클릭
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH,
                                        """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div[2]/span/button""")))
        element.click()

        # 팝업창 확인 버튼
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[3]/div/button""")))
        element.click()

        element = driver.find_element_by_xpath("""//*[@id="productForm"]/ng-include/ui-view[8]/div/div[1]/div/div/a""")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.2)

        element = driver.find_element_by_xpath(
            """//*[@id="productForm"]/ng-include/ui-view[6]/div/div[2]/div/div/div/div/div/div/input""")
        name = element.get_attribute('value')

        element = driver.find_element_by_xpath("""//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div""")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.3)

        # 상품 주요정보 탭 클릭
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="_prod-attr-section"]/div[1]/div/div/a""")))
        element.click()
        time.sleep(0.3)

        element = driver.find_element_by_xpath("""//*[@id="prd-model"]""")
        element.clear()
        element.send_keys(str(name))  # 이름 붙여넣기
        time.sleep(0.3)

        element = driver.find_element_by_xpath("""//*[@id="saleType_NEW"]""")  # 스크롤
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.5)

        # 스크롤뷰 클릭
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH,
                                        """//*[@id="_prod-attr-section"]/div[2]/div/div[5]/div/div/ncp-certification/div/div/div[1]/div[1]/div/div/div[1]""")))
        element.click()

        time.sleep(0.3)

        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH,
                                        """//*[@id="_prod-attr-section"]/div[2]/div/div[5]/div/div/ncp-certification/div/div/div[1]/div[1]/div/div/div[2]/div/div[2]/div[2]""")))
        element.click()

        while True:
            try:
                # 저장
                element = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, """//*[@id="seller-content"]/ui-view/div[3]/div[2]/div[1]/button[2]""")))
                element.click()
            except:
                time.sleep(2.0)
            else:
                break

        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[2]/div/button[2]""")))
        element.click()

        time.sleep(0.5)

        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(0.2)

        i += 1
        now = time.localtime()
        print("[%04d-%02d-%02d-%02d-%02d-%02d] %s. 상품번호: %s" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, i, pro_code))

        if i % 25 == 0:
            # 크롬 드라이버 초기화
            driver.close()

            now_dir = os.getcwd()

            # 크롤링한 웹사이트 포털
            link = 'https://sell.smartstore.naver.com/#/products/navershopping-match-product'
            # chromedriver의 경로 설정
            path = "chromedriver.exe"

            options = webdriver.ChromeOptions()
            options.add_argument('--start-fullscreen')
            options.add_experimental_option("prefs", {
                "download.default_directory": now_dir,
                "download.prompt_for_download": False,
                "donwload.directory_updrade": True
            })

            try:
                driver = webdriver.Chrome(path, options=options)
            except:
                print("Chrome driver의 파일 경로를 확인하거나 버전을 체크해 주시기 바랍니다.")

            driver.get(link)
            time.sleep(1.5)

            # 네이버 로그인 선택
            element_click(driver, """/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a""", 1.0)

            # 아이디 비밀번호 넣고 로그인
            element_send_keys(driver, """//*[@id="id"]""", account_id)
            element_send_keys(driver, """//*[@id="pw"]""", account_password)
            element_click(driver, """//*[@id="log.login"]""", 0)

            element = WebDriverWait(driver, 1000).until(
                EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""")))
            element.click()

            try:
                element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)
            except:
                element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
                element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)

            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                """//*[@id="seller-content"]/div[2]/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button"""))).click()
            except:
                time.sleep(0.5)

    driver.close()


driver = login()
pro_code_list = data_collect(driver)
change(driver, pro_code_list)
'''
while True:
    
    try:
        change(driver, pro_code_list)
    except:
        driver.close()

        now_dir = os.getcwd()

        # 크롤링한 웹사이트 포털
        link = 'https://sell.smartstore.naver.com/#/products/navershopping-match-product'
        # chromedriver의 경로 설정
        path = "chromedriver.exe"

        options = webdriver.ChromeOptions()
        options.add_argument('--start-fullscreen')
        options.add_experimental_option("prefs", {
            "download.default_directory": now_dir,
            "download.prompt_for_download": False,
            "donwload.directory_updrade": True
        })

        try:
            driver = webdriver.Chrome(path, options=options)
        except:
            print("Chrome driver의 파일 경로를 확인하거나 버전을 체크해 주시기 바랍니다.")

        driver.get(link)
        time.sleep(1.5)

        # 네이버 로그인 선택
        element_click(driver, """/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a""", 1.0)

        # 아이디 비밀번호 넣고 로그인
        element_send_keys(driver, """//*[@id="id"]""", "hdm0089")
        element_send_keys(driver, """//*[@id="pw"]""", "ghdehd123")
        element_click(driver, """//*[@id="log.login"]""", 0)

        element = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""")))
        element.click()

        try:
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)
        except:
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                                            """//*[@id="seller-content"]/div[2]/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button"""))).click()
        except:
            time.sleep(0.5)

    else:
        break
'''