from product.product_actions import enter_description, set_product_image, set_google_category, open_find_and_filter_options, set_primary_colour, block_sim_stock, activate_product, save_product, is_already_active, clean_name, check_for_save_error
from utils.selenium_utils import login, select_product, delete_firefox_bottom_banner, initialize_driver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from config.config import get_credentials
from dotenv import load_dotenv
import pandas as pd
import os
import re

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

    # Check if "completed" or "Error" column exists; if not, create it and set values to blank
    if "Completed" not in df.columns:
        df["Completed"] = ""
        df.to_excel(products_file, index=False)
    if "Error" not in df.columns:
        df["Error"] = ""
        df.to_excel(products_file, index=False)

    # Iterate through each row in products.xlsx
    for index, row in df.iterrows():
        try:
            # Check if the row is already completed; if yes, skip it
            if pd.notna(row["Completed"]) and row["Completed"]:
                continue

            item_lookup_code = row["Item Lookup Code"]

            print(f"Processing row #{index+2}/{len(df)+1} ({item_lookup_code})")

            # Select the product based on the item lookup code
            select_product(driver, wait, item_lookup_code)

            # Get Excel row data
            description = row["Ext Description"]
            image_url = row["Image URL"]
            google_category = row["Google Category"]
            primary_colour = row["Product Colour"]
            block_sim_stock_value = row["Block SIM Stock"]

            # If product is already active, display to user and skip to next
            if is_already_active(driver, wait):
                print("Product already active on Cloud MT, skipped.")
                df.at[index, "Error"] = "Product already active on Cloud MT, skipped."
                df.to_excel(products_file, index=False)
                continue

            # Populate product fields
            clean_name(driver, wait)
            enter_description(driver, wait, description)
            set_product_image(driver, image_url)
            set_google_category(driver, wait, google_category)
            open_find_and_filter_options(driver)
            set_primary_colour(driver, primary_colour, image_url)
            if block_sim_stock_value: block_sim_stock(driver)
            activate_product(driver)
            save_product(driver)
            check_for_save_error(driver)

            # Mark the row as completed and remove any previous errors
            df.at[index, "Completed"] = "TRUE"
            df.at[index, "Error"] = ""

            # Save the DataFrame with the "completed" column updated
            df.to_excel(products_file, index=False)
        except WebDriverException as er:
            print("Browser was manually closed. Or something else went wrong:", er)
            return

        except Exception as er:

            # Make error message concise
            patterns = [r"Message: (.+?)\n", r"Error: (.+?)\n"]
            matched_messages = [re.search(pattern, str(er)) for pattern in patterns]
            pretty_error_message = matched_messages[0].group(1) if any(matched_messages) else er

            print("*******************************************")
            print(f"ERROR on row {index+2}", pretty_error_message)
            df.at[index, "Error"] = str(pretty_error_message)
            df.to_excel(products_file, index=False)
            if os.environ.get("PAUSE_ON_ERROR").lower() == "true": input("Please fix the problem on the screen and press Enter to continue...")
            print("*******************************************")
            continue

    driver.quit()

if __name__ == '__main__':
    main()
