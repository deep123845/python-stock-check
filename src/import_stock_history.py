from dataclasses import dataclass
from typing import TypeAlias

month_id: TypeAlias = int #YYYYMM
sale_quantity: TypeAlias = int

@dataclass
class ProductHistory:
	upc: str
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

	parsed_lines = []

	for line in lines: 
		entries = [
			element 
			for element in line.strip('\n').split('\t') 
			if element
		]

		parsed_lines.append(entries)

	HEADER_ENTRIES = 3
	parsed_entries = []

	for i in range(len(parsed_lines)-1):
		if i == len(parsed_lines)-1:
			entries = parsed_lines[i][-HEADER_ENTRIES:] + parsed_lines[i+1][:]
		else:
			entries = parsed_lines[i][-HEADER_ENTRIES:] + parsed_lines[i+1][:-HEADER_ENTRIES]

		parsed_entries.append(entries)

	return parsed_entries