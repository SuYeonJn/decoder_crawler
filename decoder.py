# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from bs4 import BeautifulSoup


# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
import requests

# 크롬드라이버 실행
driver = webdriver.Chrome()


url = "http://decoder.kr/book-rubato/"
# 크롬 드라이버에 url 주소 넣고 실행
driver.get(url)

# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

html = driver.page_source
soup = BeautifulSoup(response.text, "html.parser")

# 내년 동월까지 반복
for months in range(0, 13):
    date = driver.find_elements(By.CLASS_NAME, "picker__day")
    time.sleep(0.5)
    first_day_index = 0

    def check_day(day):
        for i in range(0, 42):
            date_text = date[i].text
            if date_text != day:
                continue
            else:
                return i

    # 매달 1일 index 확인
    if months == 0:
        today = driver.find_element(By.CLASS_NAME, "picker__day--today")
        time.sleep(0.5)
        first_day_index = check_day(today.text)
    else:
        first_day_index = check_day("1")

    # 하루에 가능한 시간대 체크
    def check_available(date_index):
        date = driver.find_elements(By.CLASS_NAME, "picker__day")
        time.sleep(0.5)

        day = date[date_index].text

        date[date_index].click()
        time.sleep(0.5)

        time_screen = driver.find_element(By.CLASS_NAME, "ab-time-screen")
        buttons_list_all = time_screen.find_elements(By.CLASS_NAME, "ab-available-hour")
        buttons_list_disabled = time_screen.find_elements(By.CLASS_NAME, "booked")

        # 년도, 월 가져오기
        header = driver.find_element(By.CLASS_NAME, "picker__header")
        month_year = header.text

        print(len(buttons_list_all), len(buttons_list_disabled))

        # 모든 버튼 개수와 disabled된 버튼 개수 비교
        if len(buttons_list_all) != len(buttons_list_disabled):
            print(month_year, day, "취소표 발생")
        else:
            print(month_year, day, "예약 불가")

        # 모든 버튼 disabled 조사
        for i in range(len(buttons_list_all)):
            if buttons_list_all[i].is_enabled() == True:
                print(month_year, day, buttons_list_all[i].text, "취소표 발생")
            else:
                pass

    # 한 달 동안 반복
    while first_day_index < 43:
        date = driver.find_elements(By.CLASS_NAME, "picker__day")
        time.sleep(0.5)

        disabled = driver.find_elements(By.CLASS_NAME, "picker__day--disabled")
        time.sleep(0.5)

        # 다음날이 1일이면 중단, 클릭 안되면 패스
        if date[first_day_index + 1].text != "1":
            if date[first_day_index] in disabled:
                first_day_index = first_day_index + 1
            else:
                check_available(first_day_index)
                first_day_index = first_day_index + 1
        else:
            if date[first_day_index] in disabled:
                pass
            else:
                check_available(first_day_index)
            break

    # 다음달로 넘어가기
    next_month = driver.find_element(By.CLASS_NAME, "picker__nav--next")
    driver.execute_script("arguments[0].click();", next_month)
    time.sleep(4)
