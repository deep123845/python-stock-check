import csv
from dataclasses import dataclass

@dataclass
class ProudctListing:
	lcbo_number: str
	upc: str
	supplier: str
	wholesale_case_price: float
	units_per_case: int

def extract_from_quotes(input: str):
	parts = input.split('"')

	return parts[1]

def create_product_listing(row) -> ProudctListing:
	lcbo_number = extract_from_quotes(row['SKU #'])
	upc = extract_from_quotes(row['UPC'])
	supplier = row['SUPPLYING SOURCE']
	wholesale_case_price = float(extract_from_quotes(row['WHOLESALE PRICE PER CASE']))
	units_per_case = row['SELLING UNITS PER CASE']

	return ProudctListing(lcbo_number, upc, supplier, wholesale_case_price, units_per_case)

product_catalogue = []

with open('CatalogDownload_Convenience.csv') as catalogue:
	reader = csv.DictReader(catalogue, dialect='excel')
	for row in reader:
		listing = create_product_listing(row)
		product_catalogue.append(listing)

for listing in product_catalogue:
	print(listing)