from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = False
    driver = webdriver.Firefox(options=fireFoxOptions)

    # Requesting website
    print('Requesting website')
    driver.get("https://cloudmt.citruslime.com/#/products/11151")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div/div/div[2]/div/input")))

    # Sign in
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[2]/div/input').send_keys(os.environ.get("CLOUDPOS_EMAIL"))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[3]/div/input').send_keys(os.environ.get("CLOUDPOS_PASSWORD"))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[4]/button').click()

    # Go to first product
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/input")))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[1]/input').send_keys("APCC", Keys.ENTER)







if __name__ == '__main__':
    main()