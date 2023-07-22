from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium import webdriver
import time

def initialize_driver():
    fireFoxOptions = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=fireFoxOptions)
    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    return driver, wait

def login(driver: Firefox, CLOUDMT_EMAIL: str, CLOUDMT_PASSWORD: str):
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[2]/div/input').send_keys(CLOUDMT_EMAIL)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[3]/div/input').send_keys(CLOUDMT_PASSWORD)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[4]/button').click()

def select_product(driver: Firefox, wait: WebDriverWait, product_code: str):
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/input")))
    skip_to_another_item_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/input')

    # If there is already text in input, clear it
    if skip_to_another_item_input.get_attribute("value"):
        skip_to_another_item_input.clear()

    skip_to_another_item_input.send_keys(product_code, Keys.ENTER)
    time.sleep(1)
    # If product code invalid, a popup will occur. Close this and throw an error to continue to next item
    if driver.find_element(By.CSS_SELECTOR(".uk-modal.uk-open")):
        modal_message = driver.find_element(By.CSS_SELECTOR(".uk-modal.uk-open")).text
        driver.execute_script("arguments[0].remove();", driver.find_element(By.CSS_SELECTOR(".uk-modal.uk-open")))
        raise AssertionError("Error:", modal_message)
    time.sleep(2)

def delete_firefox_bottom_banner(driver: Firefox):
    firefox_bottom_banner = driver.find_element(By.XPATH, '/html/body/div/div[6]')
    driver.execute_script("arguments[0].remove();", firefox_bottom_banner)