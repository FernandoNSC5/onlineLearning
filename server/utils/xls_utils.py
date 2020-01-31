from openpyxl import load_workbook
from datetime import date

class xls_utils:

	def __init__(self):
		self.input_data = list()

	def add_to_input(self, invoice, description, customerID, country):
		#InvoiceNo	StockCode	Description	Quantity	InvoiceDate	UnitPrice	CustomerID	Country
		data = list()
		data.append(invoice)
		data.append('123123')
		data.append(description)
		data.append(1)
		data.append(str(self.get_data()))
		data.append(3.10)
		data.append(customerID)
		data.append(country)
		self.input_data.append(data)

	def flush_memory(self):
		self.input_data = list()

	def write_xls(self):
		print("[WRITING] Loading original data")
		wb = load_workbook("Online_retail.xlsx")
		ws = wb.worksheets[0]
		print("[WRITING] Appending new data")
		for row_data in self.input_data:
		    ws.append(row_data)
		print("[WRITING] Saving data")
		wb.save("Online_retail.xlsx")
		print("[WRITING] Data stored")
		self.flush_memory()

	def get_data(self):
		return date.today()

