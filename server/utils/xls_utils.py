from openpyxl import load_workbook
from datetime import date
import colorama

class xls_utils:

	def __init__(self):
		colorama.init()
		self._FORE = colorama.Fore
		self.input_data = list()

	def add_customer_data(self, invoice, stock_code, quantity, unit_price, customerID, country, description):
		data = list()
		data.append(invoice)
		data.append(stock_code)
		data.append(description)
		data.append(quantity)
		data.append(str(self.get_data()))
		data.append(unit_price)
		data.append(customerID)
		data.append(country)
		self.input_data.append(data)

	def flush_memory(self):
		self.input_data = list()

	def print_buffer(self):
		print(self.input_data)

	def write_xls(self):
		print(self._FORE.MAGENTA + "[WRITING]\tLoading original data" + self._FORE.RESET)
		wb = load_workbook("Online_retail.xlsx")
		ws = wb.worksheets[0]
		print(self._FORE.MAGENTA + "[WRITING]\tAppending new data" + self._FORE.RESET)

		#Appending data
		for row_data in self.input_data:
		    ws.append(row_data)
		
		#Saving data
		print(self._FORE.MAGENTA + "[WRITING]\tSaving data" + self._FORE.RESET)
		wb.save("Online_retail.xlsx")
		print(self._FORE.MAGENTA + "[WRITING]\tData stored" + self._FORE.RESET)
		self.flush_memory()

	def get_data(self):
		return date.today()