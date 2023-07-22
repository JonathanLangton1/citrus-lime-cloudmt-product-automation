# Citrus Lime Cloud MT Product Automation
By default, if you create a product on Cloud POS, the product will sync through to Cloud MT, but requires additional information to activate the product on the website. There is currently no bulk import functionality on Cloud MT.

This Python script will take a .xlsx input (see [products_example.xlsx](products_example.xlsx)) and activate the products on Cloud MT for you.

## Workflow:
Load products.xlsx file, and for each product, do the below:

1. Enter description
2. Insert product image
3. Set Google Category ([see options here](https://www.google.com/basepages/producttype/taxonomy-with-ids.en-GB.txt))

	**Find & filter options**

4. Set primary colour (If not specified in products.xlsx file, it will use computer vision to detect the product colour)
7. Block or unblock SIM stock ([see what this is](https://howto.citruslime.com/94790-cloud-mt/cloud-mt-activating-products-online#:~:text=Block%20SIM%20Stock,the%20supply%20chain.))

## Quick Start
Clone this repo

Copy and paste [.env.example](.env.example) and rename to `.env`. Fill out the variables inside it.

Review the steps in [main.py](main.py). You can see which functions will be run etc...

Install [Pipenv](https://pypi.org/project/pipenv/) and run the below commands

1. `pipenv shell`
2. `pipenv install`

Copy the example Excel file and populate it with your data (you can export products from Cloud POS [here](https://pos.citruslime.com/backofficeux/wizards.aspx#:~:text=Modify%20Item%20Detail%20Wizard)) - [guide](https://citrus-lime.helpjuice.com/41975-product-inventory-management/296668-using-wizards-to-make-bulk-changes-to-items)

Rename the Excel file to `products.xlsx` and place in the project directory

Run the script `python ./main.py`