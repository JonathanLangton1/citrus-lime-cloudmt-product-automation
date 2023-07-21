from product.product_actions import enter_description, set_product_image, set_google_category, open_find_and_filter_options, set_primary_colour, block_sim_stock
from utils.selenium_utils import login, select_product, delete_firefox_bottom_banner, initialize_driver
from selenium.webdriver.common.by import By
from config.config import get_credentials
from dotenv import load_dotenv


load_dotenv()

def main():
    # Fetch Cloud MT login credentials
    CLOUDMT_EMAIL, CLOUDMT_PASSWORD = get_credentials()

    # Initialise Firefox driver
    driver, wait = initialize_driver()

    # Requesting website
    driver.get("https://cloudmt.citruslime.com/#/products/1")

    # Pre-requisites
    login(driver, CLOUDMT_EMAIL, CLOUDMT_PASSWORD)
    delete_firefox_bottom_banner(driver)
    select_product(driver, wait, "APCC")

    # Populate product page
    enter_description(driver, wait, "test description")
    set_product_image(driver, "https://www.fetchclubshop.co.uk/cdn/shop/products/kong-puppy-977079_1800x1800.png")
    set_google_category(driver, wait, "Sporting Goods > Outdoor Recreation > Equestrian > Horse Care > Horse Feed")
    open_find_and_filter_options(driver)
    set_primary_colour(driver, "https://www.fetchclubshop.co.uk/cdn/shop/products/kong-puppy-977079_1800x1800.png")
    block_sim_stock(driver)

if __name__ == '__main__':
    main()