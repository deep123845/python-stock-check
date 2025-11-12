from dataclasses import dataclass
from typing import TypeAlias
import re

month_id: TypeAlias = int #YYYYMM
sale_quantity: TypeAlias = int

@dataclass
class ProductHistory:
	description: str
	stock: int
	sales: dict[month_id, sale_quantity]

def get_month_index(month_str: str) -> int:
	try:
		month, year = month_str.split('-')
		return int(f'{year}{month}')
	except ValueError:
		raise ValueError(f'Invalid month string: {month_str}')

def parse_lines(lines: list[str]) -> list[list[str]]:
	HEADER_LINES = 3

	lines = lines[HEADER_LINES:]

	parsed_lines: list[list[str]] = []

	for line in lines: 
		entries: list[str] = [
			element 
			for element in line.strip('\n').split('\t') 
			if element
		]

		parsed_lines.append(entries)

	HEADER_ENTRIES = 3
	parsed_entries: list[list[str]] = []

	for i in range(len(parsed_lines)-1):
		if i == len(parsed_lines)-1:
			entries = parsed_lines[i][-HEADER_ENTRIES:] + parsed_lines[i+1][:]
		else:
			entries = parsed_lines[i][-HEADER_ENTRIES:] + parsed_lines[i+1][:-HEADER_ENTRIES]

		parsed_entries.append(entries)

	return parsed_entries

def process_sales(entries: list[str]) -> dict[month_id, sale_quantity]:
	months: list[int] = []

	entries.reverse()

	while 1:
		entry = entries.pop()
		if re.search('^\\d{2}-\\d{4}$', entry):
			months.append(get_month_index(entry))
		
		if re.search('Sold Qty', entry):
			break

		if len(entries) == 0:
			raise Exception
		

	entries.reverse()
	sales: dict[month_id, sale_quantity] = dict()
		
	for i in range(len(months)):
		if re.search('^\\d+$', entries[i]):
			sales[months[i]] = int(entries[i])
		else:
			raise Exception

	return sales

def convert_to_product_history(lines) -> dict[ProductHistory]:
	entries = parse_lines(list(lines))
	product_histories = {}

	for entry in entries: 
		upc = entry[0]
		product_description = entry[1]
		product_stock = entry[2]
		
		try:
			sales = process_sales(entry[3:])
		except:
			raise Exception(f'Could not process sales data for {product_description}')

		product_history = ProductHistory(product_description, product_stock, sales)
		product_histories[upc] = product_history

	return product_histories