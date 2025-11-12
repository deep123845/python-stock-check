from typing import TypeAlias

month_id: TypeAlias = int #YYYYMM
sale_quantity: TypeAlias = int

def get_current_month():
	return int(202511) #temporily hardcoded

def get_current_month_ratio():
	return float(11/30) #temporily hardcoded

def get_latest_n_months(sales: dict[month_id, sale_quantity], n: int):
	included_months = list(sales.keys())
	included_months.sort(reverse=True)

	if (len(included_months) - 1) <= n:
		return included_months[:-1]

	return included_months[:n]

def calculate_average_sales(sales: dict[month_id, sale_quantity], included_months: list[month_id]):
	if len(included_months) == 0:
		return 0
	
	current_month = get_current_month()
	current_month_ratio = get_current_month_ratio()
	total_sales = 0
	total_months = 0
	for month in included_months:
		if not (month in sales.keys()):
			raise Exception(f'Month {month} not in sales {sales}')

		if month == current_month:
			total_sales += sales[month]
			total_months += current_month_ratio
		else:
			total_sales += sales[month]
			total_months += 1

	return total_sales / total_months


	

