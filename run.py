from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
from findColourForImage import findColourForImage
import requests
import time
import os

load_dotenv()

def main():

    fireFoxOptions = webdriver.FirefoxOptions()
    # fireFoxOptions.add_argument('headless')
    driver = webdriver.Firefox(options=fireFoxOptions)

    # Requesting website
    print('Requesting website')
    driver.get("https://cloudmt.citruslime.com/#/products/11151")
    wait = WebDriverWait(driver, 20)
    # wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div/div/div[2]/div/input")))

    # Sign in
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[2]/div/input').send_keys(os.environ.get("CLOUDMT_EMAIL"))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[3]/div/input').send_keys(os.environ.get("CLOUDMT_PASSWORD"))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[4]/button').click()

    # Delete firefox bottom fixed banner
    firefox_bottom_banner = driver.find_element(By.XPATH, '/html/body/div/div[6]')
    driver.execute_script("arguments[0].remove();", firefox_bottom_banner)

    # Go to first product
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/input")))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/input').send_keys("APCC", Keys.ENTER)
    time.sleep(2)

    # Enter description
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[7]/div[3]/a').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/iframe")))
    descriptionIframe = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/iframe')
    driver.switch_to.frame(descriptionIframe)
    driver.find_element(By.XPATH, '/html/body').click()
    driver.find_element(By.XPATH, '/html/body').send_keys("test description")
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[3]/button').click()

    # Set product image
    image_url = "https://www.fetchclubshop.co.uk/cdn/shop/products/kong-puppy-977079_1800x1800.png"
    # temp_file_path = "D:\coding\github\citrus-lime-cloudmt-product-automation\product_images\" + image_url.rsplit("/", 1)[-1]
    # response = requests.get(image_url)
    # with open(temp_file_path, "wb") as file:
    #     file.write(response.content)

    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[1]/div[8]/div[2]/div/div[1]/div[2]/input').send_keys("D:\coding\github\citrus-lime-cloudmt-product-automation\product_images\kong-puppy-977079_1800x1800.png")

    # Set Google Category
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div/div/div[53]")))
    driver.find_element(By.XPATH, '/html/body/div/div[4]/div[2]/div[1]/div[1]/div[11]/div[2]/div/div/div/div/div[53]').click()

    # Set find & filter options
    driver.find_element(By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[1]/div[1]/div[13]/div/div[10]').click()

    # Set primary colour
    colour = findColourForImage("product_images/kong-puppy-977079_1800x1800.png")
    print(colour)


if __name__ == '__main__':
    main()