from import_stock_history import convert_to_product_history, ProductHistory
from import_product_catalogue import convert_to_product_catalogue, ProuductListing
from sales_statistics import get_latest_n_months, calculate_average_sales
import csv
from dataclasses import dataclass
from typing import TypeAlias

month_id: TypeAlias = int #YYYYMM
sale_quantity: TypeAlias = int
@dataclass
class ProductInfo:
	upc: str
	description: str
	stock: int
	sales: dict[month_id, sale_quantity]
	lcbo_number: str
	supplier: str
	wholesale_case_price: float
	units_per_case: int

def merge_info_from_catalogue(upc: str, product_history: ProductHistory, catalogue: dict[str, ProuductListing]):
	if not (upc in catalogue):
		return
	
	return ProductInfo(
		upc = upc,
		description = product_history.description,
		stock = product_history.stock,
		sales = product_history.sales,
		lcbo_number = catalogue[upc].lcbo_number,
		supplier = catalogue[upc].supplier,
		wholesale_case_price = catalogue[upc].wholesale_case_price,
		units_per_case = catalogue[upc].units_per_case
	)

def merge_history(product_histories: dict[str, ProductHistory], catalogue: dict[str, ProuductListing]):
	product_info_dict : dict[ProductInfo] = {}

	for upc in product_histories:
		merged_info = merge_info_from_catalogue(
			upc,
			product_histories[upc],
			catalogue
		)

		if merged_info:
			product_info_dict[upc] = merged_info
	
	return product_info_dict

with open('2025-11-10-b.Txt', 'r') as x:
	a = convert_to_product_history(x)

with open('2025-11-10-c.Txt', 'r') as y:
	b = convert_to_product_history(y)

with open('2025-11-10-w.Txt', 'r') as z:
	c = convert_to_product_history(z)

d = {}

for a1 in a:
	d[a1] = a[a1]

for b1 in b:
	d[b1] = b[b1]

for c1 in c:
	d[c1] = c[c1]

with open('CatalogDownload_Convenience.csv') as catalogue:
	reader = csv.DictReader(catalogue, dialect='excel')
	e = convert_to_product_catalogue(reader)

f = merge_history(d, e)

# for upc in f:
# 	print(upc, f[upc])
upc = '675325010005'
print(f[upc].sales)

months = get_latest_n_months(f[upc].sales, 3)
salesStats = calculate_average_sales(f[upc].sales, months)

print(months)
print(salesStats)
