import csv
from dataclasses import dataclass

@dataclass
class ProuductListing:
	lcbo_number: str
	upc: str
	supplier: str
	wholesale_case_price: float
	units_per_case: int

def extract_from_quotes(input: str):
	parts = input.split('"')

	return parts[1]

def create_product_listing(row) -> ProuductListing:
	lcbo_number = extract_from_quotes(row['SKU #'])
	upc = extract_from_quotes(row['UPC'])
	supplier = row['SUPPLYING SOURCE']
	wholesale_case_price = float(extract_from_quotes(row['WHOLESALE PRICE PER CASE']))
	units_per_case = row['SELLING UNITS PER CASE']

	return ProuductListing(lcbo_number, upc, supplier, wholesale_case_price, units_per_case)

def create_product_catalogue(reader) -> ProuductListing:
	product_catalogue = []
	
	for row in reader:
		listing = create_product_listing(row)
		product_catalogue.append(listing)
	
	return product_catalogue

with open('CatalogDownload_Convenience.csv') as catalogue:
	reader = csv.DictReader(catalogue, dialect='excel')
	product_catalogue = create_product_catalogue(reader)

for listing in product_catalogue:
	print(listing)