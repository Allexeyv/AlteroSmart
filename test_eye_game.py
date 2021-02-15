from typing import Union
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import requests
import shutil
import time
from matplotlib import image as mpimg
import numpy as np

BASE_URL = 'https://www.playbuzz.com/jessicafavish10/can-you-pass-this-tricky-eye-test'
BASE_XPATH = '//*[@id="app"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div/div[3]/'
START_PATH = BASE_XPATH + 'button/div[1]/div/div/div/div/div/img'
IMG_PATH = BASE_XPATH + 'div[2]/div[2]/div[2]/div/div/div/div[{}]/div/button/div/div[1]/div[1]/div/img'
IMG_PATH_CLICK = BASE_XPATH + 'div[2]/div[2]/div[2]/div/div/div/div[{}]/div/button/div/div[1]/div[2]'
IMG_NUM = 3

project_path = Path(__file__).resolve().parent
chromedriver_path = project_path / 'chromedriver'
ADDBLOCK_PLUS_PATH = project_path / '3.10.2_0'


def download_img(image_path: str, file_name: Union[str, int]):
    """
    Downloads picture
    """
    r = requests.get(image_path, stream=True)
    r.raw.decode_content = True

    with open(file_name, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def get_avg_color(file):
    """Calculates average color in RGB of the picture and returns sum of it
    """
    a = mpimg.imread(file)
    a = np.average(a, axis=0)
    a = np.average(a, axis=0)
    return np.sum(a)


def get_img_filename(num: int):
    ext = 'jpg'
    return f'{num}.{ext}'

chrome_options = Options()
chrome_options.add_argument('load-extension=' + ADDBLOCK_PLUS_PATH.as_posix())

driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
driver.create_options()

driver.get(BASE_URL)
start_game = driver.find_element_by_xpath(START_PATH).click()

for level in range(9):
    avg_col = []
    for i in range(IMG_NUM):
        i += 1
        img_path = IMG_PATH.format(i)
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, img_path)))
        img = driver.find_element_by_xpath(img_path)
        img = img.get_attribute('src')
        download_img(img, get_img_filename(i))

        avg_col.append(get_avg_color(get_img_filename(i)))

    distances = [abs(avg_col[0] - avg_col[1]), abs(avg_col[1] - avg_col[2]), abs(avg_col[2] - avg_col[0])]
    min_distance = distances.index(min(distances))
    if min_distance == 2:
        diff_img_num = 2
    elif min_distance == 1:
        diff_img_num = 1
    else:
        diff_img_num = 3

    print(f'{level + 1} = {diff_img_num}, {avg_col}')
    driver.find_element_by_xpath(IMG_PATH_CLICK.format(diff_img_num)).click()
    time.sleep(3)

time.sleep(10)
driver.close()


