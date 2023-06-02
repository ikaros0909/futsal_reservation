# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import configparser
import calendar

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
driver.implicitly_wait(10)

#공지 닫기
driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div/div[2]/button').click()
driver.implicitly_wait(10)
driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div/div[2]/button').click()
driver.implicitly_wait(10)

checked_process = False
reserve_open = config.get('futsal', 'reserve_open')
while True:
    current_time = datetime.datetime.now()
    if current_time.day == int(reserve_open):
        # 현재가 1일이거나, 매월 말일 자정을 넘겼을 때 수행할 작업
        checked_process = True
        print("신청기간입니다. 예약작업을 수행합니다.", current_time)
        break
    else:
        # 매월 말일 자정을 넘기지 않았을 때 수행할 작업
        checked_process = False
        print("아직 신청기간이 아닙니다.:", current_time)
        time.sleep(1)


reserved = False
cycleTimeSet = 1 # delay time(초)

current_time = datetime.datetime.now()

# 현재 달의 일 수 구하기
num_days = calendar.monthrange(current_time.year, current_time.month)[1]
print("이번달 일수:", num_days, "일")

fist_day_of_month = datetime.datetime(current_time.year, current_time.month, 1) + datetime.timedelta(days=num_days) # 다음달 1일
print("다음달 1일:", fist_day_of_month)

num_days_2 = calendar.monthrange(fist_day_of_month.year, fist_day_of_month.month)[1]
print("그다음달 일수:", num_days_2, "일")

first_day_of_2month = datetime.datetime(fist_day_of_month.year, fist_day_of_month.month, 1) + datetime.timedelta(days=num_days_2) # 그 다다음달 1일

last_day_of_month = first_day_of_2month.replace(day=1) - datetime.timedelta(days=1) # 다음달 1일에서 하루를 빼서 이번달 말일을 구함
print("그다음달 말일:", last_day_of_month, "일")

# 신청 월 1일을 요일로 변환
first_weekday_number = fist_day_of_month.weekday()
print("첫 주의 요일:", first_weekday_number+2, "일")

# 신청 월 말일을 요일로 변환
last_weekday_number = last_day_of_month.weekday()
print("마지막 주의 요일:", last_weekday_number+2, "일")

x = 1 #1주/2주/3주/4주/5주

# 첫 주의 요일 구하기
if first_weekday_number >= 0 and first_weekday_number <= 5 : # 월/화/수/목/금
    y = first_weekday_number + 2
elif first_weekday_number == 6: # 일요일
    y = 1
else : 
    y = 2

# 마지막 주의 요일 구하기
if last_weekday_number >= 0 and last_weekday_number <= 5 : # 월/화/수/목/금
    last_weekday = last_weekday_number + 2
elif last_weekday_number == 6: # 일요일
    last_weekday = 1
else : 
    last_weekday = 7

# 신청월의 주 수 구하기
num_weeks = calendar.monthrange(fist_day_of_month.year, fist_day_of_month.month)[1] // 7
print("신청월의 주 수:", num_weeks, "주")

reserve_year = config.get('futsal', 'reserve_year')
reserve_month = config.get('futsal', 'reserve_month')
reserve_time = config.get('futsal', 'reserve_time') # 시간대 선택 17시~21시(10번째 시간)
reserve_ground = config.get('futsal', 'reserve_ground')

reserve_isMonday = config.get('futsal', 'reserve_isMonday')
print("월요일 예약 : ",reserve_isMonday)
reserve_isTuesday = config.get('futsal', 'reserve_isTuesday')
print("화요일 예약 : ",reserve_isTuesday)
reserve_isWednesday = config.get('futsal', 'reserve_isWednesday')
print("수요일 예약 : ",reserve_isWednesday)
reserve_isThursday = config.get('futsal', 'reserve_isThursday')
print("목요일 예약 : ",reserve_isThursday)
reserve_isFriday = config.get('futsal', 'reserve_isFriday')
print("금요일 예약 : ",reserve_isFriday)

if checked_process == True:
    
    # 대관예약
    driver.find_element(By.XPATH, '/html/body/div/div/div/section/div/ul/li[3]/a').click()
    driver.implicitly_wait(10)

    # 구장선택
    driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/ul/li[{reserve_ground}]/a").click()
    driver.implicitly_wait(10)

    # 해당월 이동
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/a[2]/img').click()
    driver.implicitly_wait(10)
    
    # 날짜확인
    print("예약날짜 체크")
    check_date = driver.find_element(By.CSS_SELECTOR, f"body > div > div > div > div:nth-child(3) > div:nth-child(2) > div.schedule-box-wrap > div.calendar-box > div > div > div:nth-child(2) > div > div > div.card-header.d-flex.justify-content-around > h5").text
    print(check_date)
    
    if f"{reserve_year}년 {reserve_month}월" in check_date: # 예약하고자 하는 달이 맞는지 확인
        print("예약가능", check_date)
        
        isFirstWeekDay = 1 # 해당 주 첫번째 선택
        loopDay = 1

        while True:
            try:
                print("#####################################################################")
                reserve_check = True
                
                if int(reserve_isMonday) == 0 and y == 2:
                    reserve_check = False
                if int(reserve_isTuesday) == 0 and y == 3:
                    reserve_check = False
                if int(reserve_isWednesday) == 0 and y == 4:
                    reserve_check = False
                if int(reserve_isThursday) == 0 and y == 5:
                    reserve_check = False
                if int(reserve_isFriday) == 0 and y == 6:
                    reserve_check = False
                
                print("reserve_check : " + str(reserve_check), y)
                if(reserve_check == False):
                    y = y + 1
                    isFirstWeekDay = 2
                    continue
                
                if y == 1 or y == 7:
                    print("###예약일이 아님[bypass]###")
                    y = 2
                    x = x + 1
                    isFirstWeekDay = 1 # 해당 주 첫번째 선택
                    continue
                else:
                    if loopDay >= last_day_of_month.day:
                        print("###모든 날짜가 예약되어 있습니다.[예약실패!]###")
                        break
                    
                    print("x : " + str(x))
                    print("y : " + str(y))
                
                    driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr/td/div/div/div[{x}]/div[{isFirstWeekDay}]/table/tbody/tr/td[{y}]").click()
                    driver.implicitly_wait(50)
                    
                    # # 요소 클릭을 위한 대기 시간 설정
                    # wait = WebDriverWait(driver, 10)
                    
                    # # 클릭하려는 요소를 식별하는 방법 (예: XPath)
                    # element_locator = (By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr/td/div/div/div[{x}]/div[1]/table/tbody/tr/td[{y}]")
                    
                    # # 요소가 클릭 가능해질 때까지 대기
                    # element = wait.until(EC.element_to_be_clickable(element_locator))

                    # # 요소 클릭
                    # element.click()

                    print("###날짜변경###")
                    time.sleep(1)
                    
                    str_date = driver.find_element(By.ID, 'str').text
                    loopDay = int(str_date[8:10])
                    
                    print(str_date) # 예약날짜
                    # print("일자 : ", int(str_date[8:10]))
                    print(driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/table/tbody/tr[{reserve_time}]/td[2]").text) # 예약시간
                    print(driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/table/tbody/tr[{reserve_time}]/td[4]/div/span[4]").text) # 예약자 정보
                    isReserveSet = driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/table/tbody/tr[{reserve_time}]/td[4]/div/span[2]").text # 예약여부
                    driver.implicitly_wait(10)
                    print(isReserveSet)
                    
                    if "예약가능" in isReserveSet:
                        print("###해당시간 예약가능###")
                        driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/table/tbody/tr[{reserve_time}]/td[1]/label").click()
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
                        # driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div[2]/div/button').click()
                        # driver.implicitly_wait(100)
                    
                        print("###예약성공!!###")
                        reserved = True
                        break
                    else:
                        # 시간대 예약 불가능
                        reserved = False
                        # time.sleep(cycleTimeSet)
                
                if not reserved:
                    print("###날짜 변경후 다시시도###")
                    loopDay = loopDay + 1
                    if y >= 6:
                        y = 2
                        x = x + 1
                        isFirstWeekDay = 1 # 해당 주 첫번째 선택
                    else:
                        y = y + 1
                        isFirstWeekDay = 2
                
                    print("isDay : " + str(loopDay), " / last_day_of_month.day : " + str(last_day_of_month.day))
                    
            except Exception as e:
                # 그 외 다른 예외가 발생한 경우 예외 처리
                print("예외가 발생했습니다:", e)
                reserved = False
                time.sleep(cycleTimeSet)
                
                # 홈으로 이동후 다시 시도
                driver.get(config.get('futsal', 'url_home')) # 이동을 원하는 페이지 주소 
                driver.implicitly_wait(15) # 페이지 다 뜰 때 까지 기다림
                time.sleep(1)
                
                #공지 닫기
                driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div/div[2]/button').click()
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div/div[2]/button').click()
                driver.implicitly_wait(10)
                
                # 대관예약
                driver.find_element(By.XPATH, '/html/body/div/div/div/section/div/ul/li[3]/a').click()
                driver.implicitly_wait(10)

                # 구장선택
                driver.find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div[2]/ul/li[{reserve_ground}]/a").click()
                driver.implicitly_wait(10)

                # 해당월 이동
                driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/a[2]/img').click()
                driver.implicitly_wait(10)

    else:
        # 해당월 예약 불가능
        print("###예약불가능!!###")
        reserved = False
        time.sleep(cycleTimeSet)
