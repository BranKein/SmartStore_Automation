# coding: utf-8

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
import os
import time
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

    return driver


def data_collect(driver):
    # 1년
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
            """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[6]/div/div/ncp-datetime-range-picker2/div[1]/div/div/button[6]""")))
    element.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3)")
    time.sleep(0.3)

    # 검색
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
            """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""")))
    element.click()
    time.sleep(1.0)

    # 전체 항목 엑셀파일 저장
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
            """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[1]/div[2]/div/div[2]/button""")))
    element.click()

    while True:
        try:
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        except:
            time.sleep(0.5)
        else:
            break

    time.sleep(3.0)

    while True:
        file_list = os.listdir('./')
        file_list = [file for file in file_list if file.endswith(".csv")]

        if len(file_list) == 1:
            break
        else:
            time.sleep(0.3)

    product_csv = pd.read_csv(file_list[0])
    os.remove(file_list[0])

    # 카탈로그 가격 엑셀파일 저장
    while True:
        try:
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        except:
            time.sleep(0.3)
        else:
            break
    time.sleep(0.3)

    try:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[4]/a""", 1.5)
    except:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[4]/a""", 1.5)

    time.sleep(0.5)

    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
        """//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div/div[1]/div[2]/div/div[2]/button""")))
    element.click()

    while True:
        try:
            element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        except:
            time.sleep(0.5)
        else:
            break

    time.sleep(3.0)

    # 카탈 csv 리드
    while True:
        file_list = os.listdir('./')
        file_list = [file for file in file_list if file.endswith(".csv")]

        if len(file_list) == 1:
            break
        else:
            time.sleep(0.3)

    best_price_product_csv = pd.read_csv(file_list[0])
    os.remove(file_list[0])

    f = open('be_170.txt', 'r', encoding="utf-8")
    be_170_str = f.read()
    f.close()

    be_170 = list()

    for i in range(len(be_170_str)):
        if be_170_str[i][-1] == '\n':
            be_170.append(be_170_str[i][:-1])

    f = open('no_sale.txt', 'r', encoding="utf-8")
    no_sale = f.readlines()
    f.close()

    for i in range(len(no_sale)):
        if no_sale[i][-1] == '\n':
            no_sale[i] = no_sale[i][:-1]

    f = open('value_const.txt', 'r', encoding="utf-8")
    const = f.readlines()
    f.close()

    consts = list()

    for i in range(len(const)):
        consts.append(const[i].split(' ')[0])

    cat = dict()

    for i in range(len(best_price_product_csv)):
        if_modify_need = True
        pro = best_price_product_csv.iloc[i]

        if pro[6] == pro[10]:
            if_modify_need = False

        if int(pro[6]) - 10 == int(pro[10]):
            if_modify_need = False

        if if_modify_need:
            cat[str(pro[0])] = int(pro[6])  # 카탈로그 최저가 저장

        if pro[2].split(' ')[0] in no_sale:
            cat[str(pro[0])] = 0

    new_modify = dict()

    for i in range(len(product_csv)):
        pro = product_csv.iloc[i]
        new_modify[str(pro[0])] = list()

        ratio = 1.0
        if str(pro[4].split(' ')[0]) in be_170:
            # 1.7로 설정
            ratio = float(consts[3])
        else:
            # 1.6으로 설정
            ratio = float(consts[2])

        # 판매가 설정
        if int(int(pro[1]) * ratio) == int(pro[10]):  # 판매가가 맞는지 확인
            new_modify[str(pro[0])].append(0)
        else:
            # 판매가를 설정해줘야 함
            new_modify[str(pro[0])].append(int(pro[1] * ratio))

        # 할인가 설정
        if str(pro[4].split(' ')[0]) not in no_sale:
            # 세일 해야함
            if str(pro[0]) in cat:
                # 카탈 최저가가 있음
                if pro[1] * float(consts[1]) < cat[str(pro[0])] - int(consts[0]):
                    # 최저가격으로 맞춰도 됨
                    if int(int(pro[1]) * ratio) == int(pro[10]):
                        # 판매가를 설정해주지 않았을 경우 원래 판매가로부터 할인가를 계산
                        if int(pro[10]) - cat[str(pro[0])] + int(consts[0]) > 0:
                            if cat[str(pro[0])] - int(consts[0]) > int(pro[1] * float(consts[1])):
                                new_modify[str(pro[0])].append(int(pro[10]) - cat[str(pro[0])] + int(consts[0]))
                            else:
                                new_modify[str(pro[0])].append(0)
                        else:
                            new_modify[str(pro[0])].append(0)
                    else:
                        # 판매가가 바뀔 예정이므로 할인가도 바뀐 판매가로부터 계산
                        if int(pro[1] * ratio) - cat[str(pro[0])] + int(consts[0]) > 0:
                            if cat[str(pro[0])] - int(consts[0]) > int(pro[1] * float(consts[1])):
                                new_modify[str(pro[0])].append(int(pro[1] * ratio) - cat[str(pro[0])] + int(consts[0]))
                            else:
                                new_modify[str(pro[0])].append(0)
                        else:
                            new_modify[str(pro[0])].append(0)
                else:
                    new_modify[str(pro[0])].append(0)
            else:
                new_modify[str(pro[0])].append(0)
        else:
            # 세일 안해도 되는 항목
            new_modify[str(pro[0])].append(0)

        if new_modify[str(pro[0])][0] == 0 and new_modify[str(pro[0])][1] == 0:
            del new_modify[str(pro[0])]
        else:
            now = time.localtime()
            print("[%04d-%02d-%02d-%02d-%02d-%02d] 상품번호: %s, 상품코드: %s, 판매가(0인경우 변경없음): %s, 할인금액(0인경우 변경없음): %s" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, pro[0], pro[1], new_modify[str(pro[0])][0], new_modify[str(pro[0])][1]))

    print()
    now = time.localtime()
    print("[%04d-%02d-%02d-%02d-%02d-%02d] 수정해야 하는 항목은 총 %s개 입니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, len(new_modify)))

    return new_modify


def price_manage(modify):
    global driver
    global i

    try:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)
    except:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)
    
    time.sleep(0.5)

    for pro_code in modify.keys():
        
        # 상품번호 입력
        textarea = driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea""")
        textarea.clear()
        textarea.send_keys(pro_code)
        time.sleep(0.3)
    
        # 검색
        driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""").click()
        time.sleep(1.0)
    
        # 수정 버튼 클릭
        element = driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[3]/div/button""")  # 스크롤
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.3)


        element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div/div[2]/span/button""")))
        element.click()

        while True:
            try:
                # 팝업창 확인 버튼
                element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[3]/div/button""")))
                element.click()
            except:
                time.sleep(0.5)
            else:
                break
    
        element = driver.find_element_by_xpath("""//*[@id="productForm"]/ng-include/ui-view[8]/div/div[1]/div/div/a""")
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.2)
    
        if modify[pro_code][0] != 0:
            # 판매가 설정
            element = driver.find_element_by_xpath("""//*[@id="prd_price2"]""")
            element.clear()
            element.send_keys(str(modify[pro_code][0]))
            time.sleep(0.3)
    
        if modify[pro_code][1] != 0:
            # 할인 설정하기 버튼
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="price-benefit"]/div[2]/div/fieldset/div/div/div[1]/label[1]""")))
            element.click()
        
            time.sleep(0.2)
    
            element = driver.find_element_by_xpath("""//*[@id="prd_sale"]""")
            element.clear()
            element.send_keys(str(modify[pro_code][1]))
        
            time.sleep(0.3)

        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(0.3)

        while True:
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div[3]/div[2]/div[1]/button[2]/span[1]""")))
                element.click()
            except:
                time.sleep(0.3)
            else:
                break

        time.sleep(0.5)

        i += 1

        try:
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[2]/div/button[2]""")))
            element.click()
        except:
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[2]/div/span/button""")))
            element.click()

            now = time.localtime()
            print("[%04d-%02d-%02d-%02d-%02d-%02d] %s. 상품번호: %s 실패" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, i, pro_code))

            # alert

            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div[3]/div[2]/div[2]/button[2]""")))
            element.click()

            Alert(driver).accept()
            time.sleep(0.3)
        else:
            time.sleep(1.0)
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

    driver.close()
    return 0


while True:
    now = time.localtime()
    print("[%04d-%02d-%02d-%02d-%02d-%02d] 카탈로그 가격관리를 시작합니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    print()

    driver = login()
    new_modify = data_collect(driver)

    i = 0

    while True:
        result = price_manage(new_modify)

        if result == 0:
            break
        else:
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
            continue

    print()
    now = time.localtime()
    print("[%04d-%02d-%02d-%02d-%02d-%02d] 카탈로그 가격관리가 완료되었습니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    now = time.localtime()
    print("[%04d-%02d-%02d-%02d-%02d-%02d] 1시간동안 휴식합니다..." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    print()
    time.sleep(3600.0)

