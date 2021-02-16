from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


BASE_URL = 'https://www.playbuzz.com/jessicafavish10/can-you-pass-this-tricky-eye-test'
BASE_XPATH = '//*[@id="app"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div/div[3]/'
START_PATH = BASE_XPATH + 'button/div[1]/div/div/div/div/div/img'
IMG_PATH = BASE_XPATH + 'div[2]/div[2]/div[2]/div/div/div/div[{}]/div/button/div/div[1]/div[1]/div/img'
IMG_PATH_CLICK = BASE_XPATH + 'div[2]/div[2]/div[2]/div/div/div/div[{}]/div/button/div/div[1]/div[2]'
FINAL_TEXT = 'You Passed!!!'
SCREENSHOT = 'succeed.png'
IMG_NUM = 3
ANSWERS = [3, 2, 3, 1, 1, 2, 3, 2, 1]


def test_win_game(driver):
    """Test wins the game 'can-you-pass-this-tricky-eye-test' by selecting the right answers.
    """
    driver.get(BASE_URL)
    driver.find_element_by_xpath(START_PATH).click()

    for level in range(9):
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, IMG_PATH.format(IMG_NUM)))
        )
        driver.find_element_by_xpath(IMG_PATH_CLICK.format(ANSWERS[level])).click()

    time.sleep(10)
    assert driver.page_source.find(FINAL_TEXT)
    driver.save_screenshot(SCREENSHOT)
    driver.close()
