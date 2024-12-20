"""
TODO: Организовать считывание оценок из двойных блоков (две оценки в один день)
Можно брать XPATH родительского элемента оценки и на его основе создавать XPATH для веса
"""


import time
import os
import configparser 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class Parser:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("force-device-scale-factor=0.1")

    driver = webdriver.Chrome(options=chrome_options)

    def auth_to_og1(self):
        driver = self.driver
        config = configparser.ConfigParser() 

        config.read(fr"{os.path.dirname(os.path.abspath(__file__))}\settings.ini")

        auth_url = "https://lms.og1.ru/signin"
        email = config.get('SCHOOL_ACCOUNT', 'email')
        password = config.get('SCHOOL_ACCOUNT', 'password')

        driver.get(auth_url)
        driver.maximize_window()
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div/div/input'))
        )
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[1]/div/div/input').send_keys(email)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/div/input').send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[1]/div/div[3]/button/div/span').click()

        while driver.current_url != "https://lms.og1.ru/":
            pass

    def parsing(self):
        driver = self.driver
        config = configparser.ConfigParser() 

        config.read(fr"{os.path.dirname(os.path.abspath(__file__))}\settings.ini")

        self.auth_to_og1()

        performance_url = "https://lms.og1.ru/performance?quarter=0"
        driver.get(performance_url)
        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="AcademicPerformance"]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div')))
        time.sleep(0.4)
        actions = ActionChains(driver) 
        for date_marks in driver.find_elements(By.CLASS_NAME, "pt-table-dates-marks"):
            for cur_block in date_marks.find_elements(By.CLASS_NAME, "pt-table-marks"):
                try:
                    element = cur_block.find_element(By.CLASS_NAME, "mark-group")
                    if element.text == "":
                        continue
                except NoSuchElementException:
                    continue
                grade = element.text
                time.sleep(0.2)
                # driver.execute_script("arguments[0].scrollIntoView(true);", element)
                actions.move_to_element(element).perform()
                time.sleep(0.2)
                try:
                    WebDriverWait(cur_block, 1.3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "mark-weight"))
                    )
                    weight = cur_block.find_element(By.CLASS_NAME, "mark-weight").text
                    print(f"{grade};{weight}")
                except NoSuchElementException:
                    print(f"{grade}; weight not found")
                except TimeoutException:
                    print("!!!!!")
                    # print(f"{grade}; weight did not load in time")
                    try:
                        element = cur_block.find_element(By.CLASS_NAME, "mark-group")
                        actions.move_to_element(element).perform()
                        tooltip = cur_block.find_element(By.CLASS_NAME, "tooltip-meta-data").text
                        weight = tooltip[-4:-1]
                        if weight[0] == "с":
                            weight = weight[2::]
                        print(f"{grade};{weight}")
                    except (TimeoutException, NoSuchElementException):
                        print(f"{grade}; weight did not load in time")
        driver.quit()

if __name__ == "__main__":
    Parser().parsing()