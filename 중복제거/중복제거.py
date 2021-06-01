from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys
import time
import numpy as np
import pandas as pd


print()
print("이 프로그램은 김연혁 이 제작한 프로그램입니다.")
print()
account_id = input("네이버 아이디를 입력해주세요: ")
account_password = input("네이버 비밀번호를 입력해주세요: ")
print()


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

# xpath에 해당하는 element를 클릭하고 원하는 만큼 대기하는 함수
def element_click(driver, xpath, sleep):
    driver.find_element_by_xpath(xpath).click()
    time.sleep(sleep)


# xpath에 해당하는 element에 원하는 문자열을 send하는 함수
def element_send_keys(driver, xpath, string):
    element = driver.find_element_by_xpath(xpath)
    element.send_keys(string)

#네이버 아이디로 로그인
element_click(driver, """/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a""", 1.0)

# 로그인
element_send_keys(driver, """//*[@id="id"]""", account_id)
element_send_keys(driver, """//*[@id="pw"]""", account_password)
element_click(driver, """//*[@id="log.login"]""", 0)

while True:
    try:
        element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
    except:
        time.sleep(0.5)
    else:
        break

try:
    element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)
except:
    element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/a""", 0.5)
    element_click(driver, """//*[@id="seller-lnb"]/div/div[1]/ul/li[1]/ul/li[1]/a""", 1.5)

driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[6]/div/div/ncp-datetime-range-picker2/div[1]/div/div/button[6]""").click() # 1년
time.sleep(0.1)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3)")
time.sleep(0.3)

# 검색
driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""").click()
time.sleep(1.0)

# 전체 항목 엑셀파일 저장
driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[1]/div[2]/div/div[2]/button""").click()

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

delete_list = list()
check_dict = dict()

for i in range(len(product_csv)):
    pro = product_csv.iloc[i]

    pro_num = str(pro[0])
    pro_code = str(pro[1])
    name = pro[4]
    brand = pro[4].split(' ')[0]
    remain = str(pro[9])
    value = str(pro[10])
    register_date = str(pro[54])
    modify_date = str(pro[55])

    if brand in check_dict:
        if name not in check_dict[brand]:
            check_dict[brand][name] = list()
    else:
        check_dict[brand] = dict()
        check_dict[brand][name] = list()

    check_dict[brand][name].append((pro_num, pro_code, name, remain, value, register_date, modify_date))

for brand in check_dict.keys():
    for product in check_dict[brand].keys():
        p = check_dict[brand][product]

        # 중복상품 두개
        if len(p) == 2:
            if p[0][1] == p[1][1]:
                # 일반적 중복상품, 앞에꺼 지우기
                delete_list.append(p[0][0])

driver.execute_script("window.scrollTo(0, 0)")

if len(delete_list) == 0:
    print("중복상품이 없습니다. 프로그램을 종료합니다.")
    driver.close()
    sys.exit()

delete_str = ""
for i in delete_list:
    delete_str += (i + ",")
delete_str = delete_str[:-1]

# 상품들 입력
textarea = driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea""")
textarea.clear()
textarea.send_keys(delete_str)
time.sleep(0.5)

element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""")))
element.click()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3)")
time.sleep(0.3)

# 전체 선택
element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/span""")))
element.click()

# 선택 삭제 버튼
element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button""")))
element.click()

# 삭제 확인 버튼
element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[2]/div/span[2]/button""")))
element.click()

# 변경결과 탭 엑스
element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[1]/div/div/div[1]/button""")))
element.click()

driver.execute_script("window.scrollTo(0, 0)")

# 클리어
textarea = driver.find_element_by_xpath("""//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea""")
textarea.clear()

element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[1]/div[2]/form/div[2]/div/button[1]""")))
element.click()

# 전체 항목 엑셀파일 저장
element = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/ui-view/div/ui-view[2]/div[1]/div[1]/div[2]/div/div[2]/button""")))
element.click()


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

delete_list = list()
check_dict = dict()

for i in range(len(product_csv)):
    pro = product_csv.iloc[i]

    pro_num = str(pro[0])
    pro_code = str(pro[1])
    name = pro[4]
    brand = pro[4].split(' ')[0]
    remain = str(pro[9])
    value = str(pro[10])
    register_date = str(pro[54])
    modify_date = str(pro[55])

    if brand in check_dict:
        if name not in check_dict[brand]:
            check_dict[brand][name] = list()
    else:
        check_dict[brand] = dict()
        check_dict[brand][name] = list()

    check_dict[brand][name].append((pro_num, pro_code, name, remain, value, register_date, modify_date))

f = open('delete_list.txt', 'w')
for brand in check_dict.keys():
    for product in check_dict[brand].keys():
        if len(check_dict[brand][product]) != 1:
            for i in check_dict[brand][product]:
                f.write("{} 상품코드: {} 상품명: {} 재고수량: {} 판매가: {} 상품등록일: {} 최종수정일: {}\n".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            f.write("\n")
f.close()

driver.close()