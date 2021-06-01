# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import time
import openpyxl
import requests


# xpath에 해당하는 element에 원하는 문자열을 send하는 함수
def element_send_keys(driver, xpath, string):
    element = driver.find_element_by_xpath(xpath)
    element.send_keys(string)


print()
print("이 프로그램은 김연혁 이 제작한 프로그램입니다.")
print()
account_id = input("네이버 아이디를 입력해주세요: ")
account_password = input("네이버 비밀번호를 입력해주세요: ")
print()


def login():
    now_dir = os.getcwd()

    # 크롤링한 웹사이트 포털
    link = 'https://sell.smartstore.naver.com/#/naverpay/sale/delivery'
    # chromedriver의 경로 설정
    path = "chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_argument('--start-fullscreen')
    options.add_experimental_option("prefs", {
        "download.default_directory": now_dir,
        "download.prompt_for_download": False,
        "donwload.directory_updrade": True
    })

    driver = webdriver.Chrome(path, chrome_options=options)

    driver.get(link)
    time.sleep(1.5)

    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, """/html/body/ui-view[1]/div[3]/div/div/div/form/div[1]/ul/li[2]/a"""))).click()
    time.sleep(1.0)

    element_send_keys(driver, """//*[@id="id"]""", account_id)
    element_send_keys(driver, """//*[@id="pw"]""", account_password)
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="log.login"]"""))).click()

    time.sleep(1.0)

    return driver


def get_order_data(driver):
    time.sleep(3.0)

    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="seller-content"]/div/div/div/div[1]/ncp-manager-notice-view/ng-transclude/button"""))).click()
    except:
        time.sleep(0.5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3)")

    iframe = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="__naverpay"]""")))

    driver.switch_to.frame(iframe)

    # 전체 항목 엑셀파일 저장

    element = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="__app_root__"]/div/div[2]/div[3]/div[1]/div/button[2]""")))
    element.click()

    time.sleep(2)

    return driver


def send_message(driver):
    while True:
        file_list = os.listdir('./')
        file_list = [file for file in file_list if file.endswith(".xlsx") and file != 'message_send.xlsx']

        if len(file_list) == 1:
            break
        else:
            time.sleep(0.3)

    load_ws = openpyxl.load_workbook(file_list[0], data_only=True)['발주발송관리']
    os.remove(file_list[0])

    driver.close()

    datas = []
    for row in load_ws.rows:
        row_value = []
        for cell in row:
            row_value.append(str(cell.value))
        datas.append(row_value)

    del datas[0]
    del datas[0]

    # datas[][0] : 상품주문번호
    # datas[][8] : 구매자명 (이름+전화번호뒷자리)
    # datas[][43] : 구매자연락처
    # datas[][16] : 상품명
    # datas[][18] : 옵션
    # datas[][20] : 수량
    # datas[][25] : 가격
    # datas[][37] : 상품코드
    # datas[][10] : 수취인명
    # datas[][40] : 수취인연락처1
    # datas[][41] : 수취인연락처2
    # datas[][42] : 주소
    # datas[][45] : 배송메세지

    log_const = [0, 8, 16, 18, 20, 37, 100, 10, 40, 41, 42, 45]

    # 신규주문 데이터 가져오기 끝

    load_wb = openpyxl.load_workbook('message_send.xlsx', data_only=True)
    load_ws = load_wb['Sheet1']


    send_log = []
    for row in load_ws.rows:
        row_value = []
        for cell in row:
            row_value.append(str(cell.value))
        send_log.append(row_value)

    del send_log[0]

    print(len(send_log))

    unsent_order = []  # 스마트스토어에서 가져온 데이터 중 log에 없는 신규주문들 저장
    append_send_log = []  # log에 없는 신규주문을 정제해서 다시 저장

    for order in datas:
        if_in = 0
        for log in send_log:
            if log[0] == order[0]:
                if_in = 1  # 신규주문이 아닌 경우 체크

        # 신규주문인 경우
        if if_in == 0:
            unsent_order.append(order)

            # log에 넣을 정제된 데이터 생성
            new_log = []
            for num in log_const:
                if num != 100:
                    new_log.append(order[num])
                else:
                    new_log.append("")

            new_log[1] += order[43].split('-')[-1]
            new_log[7] += order[43].split('-')[-1]

            if new_log[9] == 'None':
                new_log[9] = ""

            append_send_log.append(new_log)

    send_list = []  # 전화번호만 저장

    for order in unsent_order:
        if order[43] not in send_list:
            send_list.append(order[43])

    if len(send_list) == 0:
        return 0

    print('토큰 발급 중')

    # 토큰 발급

    token_get_url = 'https://kakaoapi.aligo.in/akv10/token/create/30/s/'

    token_get_json = {'apikey': 'apikey',  # api key
                      'userid': 'userid'  # 알리고 사이트 아이디
                      }

    while True:
        create_token_response = requests.post(token_get_url, data=token_get_json)
        print(create_token_response.json())
        print()
        if create_token_response.json()['code'] == 0:
            break
        else:
            time.sleep(1.0)

    # 카카오톡 보내기

    send_message_url = 'https://kakaoapi.aligo.in/akv10/alimtalk/send/'

    # ================================================================== 알림톡 보낼 때 필수 key값
    # API key, userid, token, senderkey, tpl_code, sender, receiver_1, subject_1, message_1
    # API키, 알리고 사이트 아이디, 토큰, 발신프로파일 키, 템플릿 코드, 발신번호, 수신번호, 알림톡 제목, 알림톡 내용

    sms_data = dict()
    sms_data['apikey'] = 'apikey'
    sms_data['userid'] = 'userid'
    sms_data['token'] = create_token_response.json()['token']
    sms_data['senderkey'] = 'senderkey'
    sms_data['tpl_code'] = 'tpl_code'
    sms_data['sender'] = 'phone_number'

    for i, send in enumerate(send_list):
        sms_data['receiver_' + str(i+1)] = send
        sms_data['subject_' + str(i+1)] = "상품 구매 후 문자 " + send
        sms_data['message_' + str(i+1)] = """문자 보낼거들"""

    alimtalk_send_response = requests.post(send_message_url, data=sms_data)
    if alimtalk_send_response.json()['code'] != 0:
        print(alimtalk_send_response.json())

    print("알림톡 발송 완료, 로그 저장")
    print()

    for log in append_send_log:
        load_ws.append(log)

    load_wb.save('message_send.xlsx')

    return len(send_list)


while True:
    driver = login()
    try:
        driver = get_order_data(driver)
    except:
        driver = login()
    count = send_message(driver)
    now = time.localtime()
    print("[%04d-%02d-%02d-%02d-%02d-%02d] %d명에게 문자를 보냈습니다. 10분간 휴식을 시작합니다." % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, count))
    time.sleep(600.0)

