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

def is_already_active(driver: Firefox, wait: WebDriverWait):
    time.sleep(1)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".page-loading-visible")))
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[2]/span")))
    isCheckboxSelected = "Not active" not in driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[2]/span').text
    return isCheckboxSelected

def clean_name(driver: Firefox, wait: WebDriverWait):
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[4]/div[2]/input")))
    product_name = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[4]/div[2]/input').get_attribute("value")
    clean_product_name = product_name.replace("&", "and").replace("(", "-").replace(")", "")
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[4]/div[2]/input').clear()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[4]/div[2]/input').send_keys(clean_product_name)

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
    filename = clipped_url.rsplit("/", 1)[-1]
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "product_images", filename)
    response = requests.get(clipped_url)
    with open(file_path, "wb") as file:
        file.write(response.content)

    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[8]/div[2]/div/div[1]/div[2]/input').send_keys(file_path)
    check_for_popup(driver)

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

    file_path = "product_images\\" + clipped_url.rsplit("/", 1)[-1]
    if (colourIsNotSpecified):
        colour = find_colour_for_image(file_path)
    else:
        colour = primary_colour
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[2]/ul[2]/li[1]/div[5]/div[2]').click()
    driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[2]/ul[2]/li[1]/div[5]/div[2]/div/div/div[@data-value="{colour}"]').click()

    if (os.path.isfile(file_path)):
        os.remove(file_path)

def set_item_group(driver: Firefox, item_group: str):
    if not item_group:
        return
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[2]/ul[2]/li[1]/div[7]/div[3]/div[2]').click()
    driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[2]/ul[2]/li[1]/div[5]/div[2]/div/div/div[contains(string(), "{item_group}")]').click()

def close_find_and_filter_options(driver: Firefox):
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]/div/div/div/div/div/div[3]/button').click()

def block_sim_stock(driver: Firefox):
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[16]/div[2]/div[9]/div[2]/input').click()

def activate_product(driver: Firefox):
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[2]/input').click()

def save_product(driver: Firefox):
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[3]/button[2]').click()

def check_for_save_error(driver: Firefox):
    check_for_popup(driver)
    
def check_for_popup(driver: Firefox):
    time.sleep(1)
    if driver.find_elements(By.CSS_SELECTOR, ".uk-modal.uk-open"):
        modal_message = driver.find_element(By.CSS_SELECTOR, ".uk-modal-body").text
        driver.execute_script("arguments[0].remove();", driver.find_element(By.CSS_SELECTOR, ".uk-modal.uk-open"))
        raise AssertionError("Error:", modal_message)