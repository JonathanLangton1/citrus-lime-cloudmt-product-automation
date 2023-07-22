from product.product_actions import enter_description, set_product_image, set_google_category, open_find_and_filter_options, set_primary_colour, block_sim_stock
from utils.selenium_utils import login, select_product, delete_firefox_bottom_banner, initialize_driver
from selenium.webdriver.common.by import By
from config.config import get_credentials
from dotenv import load_dotenv
import pandas as pd
import os

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

    # Read data from the products.xlsx file
    products_file = "products.xlsx"
    if not os.path.exists(products_file):
        print("products.xlsx file not found.")
        return

    df = pd.read_excel(products_file)

    # Check if "completed" column exists; if not, create it and set values to blank
    if "Completed" not in df.columns:
        df["Completed"] = ""
        df.to_excel(products_file, index=False)

    # Iterate through each row in products.xlsx
    for index, row in df.iterrows():
        try:
            # Check if the row is already completed; if yes, skip it
            if pd.notna(row["Completed"]) and row["Completed"]:
                continue

            item_lookup_code = row["Item Lookup Code"]

            # Select the product based on the item lookup code
            select_product(driver, wait, item_lookup_code)

            # Get Excel row data
            description = row["Ext Description"]
            image_url = row["Image URL"]
            google_category = row["Google Category"]
            primary_colour = row["Product Colour"]
            block_sim_stock_value = row["Block SIM Stock"]

            # Populate product fields
            enter_description(driver, wait, description)
            set_product_image(driver, image_url)
            set_google_category(driver, wait, google_category)
            open_find_and_filter_options(driver)
            set_primary_colour(driver, primary_colour, image_url)
            if block_sim_stock_value: block_sim_stock(driver)

            # Mark the row as completed
            df.at[index, "Completed"] = "TRUE"

            # Save the DataFrame with the "completed" column updated
            df.to_excel(products_file, index=False)
        except Exception as er:
            print(er)
            continue

if __name__ == '__main__':
    main()
