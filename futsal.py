# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import configparser

# 설정 파일을 읽어들입니다.
config = configparser.ConfigParser()
config.read('config.ini')

driver = webdriver.Chrome("chromedriver") # Webdriver 파일의 경로를 입력
driver.get(config.get('futsal', 'url')) # 이동을 원하는 페이지 주소 
driver.implicitly_wait(15) # 페이지 다 뜰 때 까지 기다림

driver.find_element(By.ID, 'id').send_keys(config.get('futsal', 'id')) # 회원번호
driver.find_element(By.ID, 'pwd').send_keys(config.get('futsal', 'pwd')) # 비밀번호

# 로그인
driver.find_element(By.XPATH, '/html/body/div/div/div/section/div/div[2]/div[1]/div[2]/button').click()
driver.implicitly_wait(5)

#공지 닫기
driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div/div[2]/button').click()
driver.implicitly_wait(5)
driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div/div[2]/button').click()
driver.implicitly_wait(5)

current_time = datetime.datetime.now()
last_day_of_month = datetime.datetime(current_time.year, current_time.month, 1) + datetime.timedelta(days=32) # 다음달 1일
last_day_of_month = last_day_of_month.replace(day=1) - datetime.timedelta(days=1) # 다음달 1일에서 하루를 빼서 이번달 말일을 구함

checked_process = False
while True:
    current_time = datetime.datetime.now()
    if current_time.day == 1 or current_time > last_day_of_month.replace(hour=23, minute=59, second=59):
        # 현재가 1일이거나, 매월 말일 자정을 넘겼을 때 수행할 작업
        checked_process = True
        print("매월 말일 자정을 넘겼습니다. 예약작업을 수행합니다.")
        break
    else:
        # 매월 말일 자정을 넘기지 않았을 때 수행할 작업
        checked_process = False
        print("아직 매월 말일 자정을 넘기지 않았습니다.:", last_day_of_month, current_time)
        time.sleep(1)


reserved = False
cycleTimeSet = 1 # delay time(초)

x = 2 #1주/2주/3주/4주/5주
y = 2 #월/화/수
i = 10 # 시간대 선택 17시~21시(10번째 시간)
if checked_process == True:
    while True:
        try:
            # 대관예약
            driver.find_element(By.XPATH, '/html/body/div/div/div/section/div/ul/li[3]/a').click()
            driver.implicitly_wait(10)

            # 5구장
            driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/ul/li[6]/a').click()
            driver.implicitly_wait(10)

            # 7월이동
            driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/a[2]/img').click()
            driver.implicitly_wait(10)

            # 날짜확인
            print("예약날짜 체크")
            check_date = driver.find_element(By.CSS_SELECTOR, f"body > div > div > div > div:nth-child(3) > div:nth-child(2) > div.schedule-box-wrap > div.calendar-box > div > div > div:nth-child(2) > div > div > div.card-header.d-flex.justify-content-around > h5").text
            print(check_date)
            
            if config.get('futsal', 'reserve_month') in check_date: # 예약하고자 하는 달이 맞는지 확인

                print("###예약오픈###")

                # /html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr/td/div/div/div[행]/div[2]/table/thead/tr/td[열]/span
                # 첫째주 월요일 선택
                driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr/td/div/div/div[{x}]/div[1]/table/tbody/tr/td[{y}]").click()
                driver.implicitly_wait(10)

                check_time = driver.find_element(By.CSS_SELECTOR, f"body > div > div > div > div:nth-child(3) > div:nth-child(2) > table > tbody > tr:nth-child({i}) > td:nth-child(4) > div").text
                print(check_time)
                if "예약가능" in check_time:
                    print("###시간가능###")
                    driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[1]/label").click()
                    driver.implicitly_wait(10)
                    
                    # 다음단계
                    print("###다음단계###")
                    driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/div[2]/button[2]").click()
                    driver.implicitly_wait(10)
                    
                    # 이용내역 동의
                    print("###이용내역조회###")
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[2]/div[4]/div[1]/label/span').click()
                    driver.implicitly_wait(10)
                    
                    # 예약신청
                    print("###예약신청###")
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[2]/div[4]/div[2]/button[2]').click()
                    driver.implicitly_wait(10)
                    
                    # 예약신청
                    print("###최종신청###")
                    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[2]/div/button').click()
                    driver.implicitly_wait(100)
                
                    print("###예약성공!!###")
                    reserved = True
                    break
                else:
                    # 시간대 예약 불가능
                    reserved = False
                    time.sleep(cycleTimeSet)
                
            else:
                # 해당월 예약 불가능
                reserved = False
                time.sleep(cycleTimeSet)
            
            if not reserved:
                print("새로고침")
                
                # 예약현황/취소
                driver.find_element(By.XPATH, '/html/body/div/div/div/section/div/ul/li[2]/a').click()
                driver.implicitly_wait(10)
                
                if y == 6:
                    y = 2
                    x = x + 1
                else:
                    y = y + 1
            
                print("x : " + str(x))
                print("y : " + str(y))
            else:
                break
            
        except Exception as e:
            # 그 외 다른 예외가 발생한 경우 예외 처리
            print("예외가 발생했습니다:", e)
            reserved = False
            time.sleep(cycleTimeSet)