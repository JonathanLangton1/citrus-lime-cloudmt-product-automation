from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.image_utils import find_colour_for_image
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from urllib.parse import urlparse
import requests
import time
import math
import os

def enter_description(driver: Firefox, wait: WebDriverWait, description: str):
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[7]/div[3]/a")))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[7]/div[3]/a').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/iframe")))
    descriptionIframe = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/iframe')
    driver.switch_to.frame(descriptionIframe)
    driver.find_element(By.XPATH, '/html/body').click()
    driver.find_element(By.XPATH, '/html/body').send_keys(description)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[3]/button').click()

def set_product_image(driver: Firefox, image_url: str):
    clipped_url = f"{urlparse(image_url).scheme}://{urlparse(image_url).netloc}{urlparse(image_url).path}"
    file_path = "D:\coding\github\citrus-lime-cloudmt-product-automation\product_images\\" + clipped_url.rsplit("/", 1)[-1]
    response = requests.get(clipped_url)
    with open(file_path, "wb") as file:
        file.write(response.content)

    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[8]/div[2]/div/div[1]/div[2]/input').send_keys(file_path)

def set_google_category(driver: Firefox, wait: WebDriverWait, category: str):
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div")))
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div/div/div[@data-value="{category}"]')))
    driver.find_element(By.XPATH, f'/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div/div/div[@data-value="{category}"]').click()

def open_find_and_filter_options(driver: Firefox):
    driver.find_element(By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]').click()

def set_primary_colour(driver: Firefox, primary_colour, image_url: str):

    clipped_url = f"{urlparse(image_url).scheme}://{urlparse(image_url).netloc}{urlparse(image_url).path}"

    colourIsNotSpecified = (
        isinstance(primary_colour, (float, int)) and math.isnan(primary_colour)
    ) or primary_colour == "DETECT"

    if (colourIsNotSpecified):
        file_path = "product_images\\" + clipped_url.rsplit("/", 1)[-1]
        colour = find_colour_for_image(file_path)
    else:
        colour = primary_colour
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[2]/ul[2]/li[1]/div[7]/div[3]/div[2]').click()
    driver.find_element(By.XPATH, f'/html/body/div/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[2]/ul[2]/li[1]/div[7]/div[3]/div[2]/div/div/div[@data-value="{colour}"]').click()
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[3]/button').click()

    if (os.path.isfile(file_path)):
        os.remove(file_path)

def block_sim_stock(driver: Firefox):
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[16]/div[2]/div[9]/div[2]/input').click()