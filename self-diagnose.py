# -*- coding: utf-8 -*-
from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
import logging


school: str = "school"  # 학교이름
name: str = "name"  # 이름
birth_date: str = "YYMMDD"  # 생년월일
path_to_driver: str = 'chromedriver.exe'  # ChromeDriver 경로
time: str = "HH:MM"  # 진단 시각

logging.basicConfig(level=logging.INFO,
                    filename='diagnose.log',
                    filemode='a',
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
logging.getLogger().addHandler(console)

diagnose_logger = logging.getLogger('diagnose')


def diagnose():
    diagnose_logger.info("starting self diagnosis")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options, executable_path=path_to_driver)
    driver.implicitly_wait(.5)
    driver.get("https://eduro.goe.go.kr/hcheck/index.jsp")

    # 본인확인 방법 선택
    driver.find_element_by_xpath("/html/body/app-root/div[2]/section/div/div/div/div[2]/div/a[2]/div").click()

    # 학생정보 입력
    driver.find_element_by_name("schulNm").send_keys(school)
    driver.find_element_by_name("pName").click()
    while not (name in driver.find_element_by_name("pName").get_attribute("value")):
        driver.find_element_by_name("pName").send_keys(name)

    driver.find_element_by_name("frnoRidno").send_keys(birth_date)
    driver.find_element_by_id("btnConfirm").click()

    # 설문조사 진행
    for num in map(str, [1, 2, 7, 8, 9]):
        driver.find_element_by_name("rspns0" + num).click()
    driver.find_element_by_id("btnConfirm").click()

    # 완료 메시지 출력
    diagnose_logger.info(driver.find_element_by_class_name("content_box").text.replace('\n', ' '))

    diagnose_logger.info("self diagnosis complete")
    driver.quit()


schedule = BlockingScheduler()
schedule.add_job(diagnose, 'cron', day_of_week='0-4', hour=time.split(':')[0], minute=time.split(':')[1])

schedule.start()
