
class DataConverter(object):

	def __init__(self, input_file_path, output_file_path, col_mapping):
		self.input_file_path = input_file_path
		self.output_file_path = output_file_path
		self.col_mapping = col_mapping

		self.csv_reader = None
		self.csv_writer = None


	def convert(self):

		input_file = open(self.input_file_path, 'rb')
		self.csv_reader = csv.reader(input_file)

		output_file = open(self.output_file_path, 'wb')
		self.csv_writer = csv.writer(output_file)

		self.process_data(self.csv_reader, self.csv_writer)

		input_file.close()
		output_file.close()

	def process_data(self, csv_reader, csv_writer):
		pass
