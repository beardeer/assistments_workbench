

import csv
from ASSISTments-data-workbench import problem_difficulty


probelm_diff_dict = {}

def generate_PFA_data(input_file_path, output_file_path, col_mapping = {}, pfa_model = 1):
	input_file = open(input_file_path, 'rb')
	csv_reader = csv.reader(input_file)

	output_file = open(output_file_path, 'wb')
	csv_writer = csv.writer(output_file)

	header = reader.next()
	print header

	user_col = col_mapping['user_id']
	seq_col = col_mapping['sequence_id']
	problem_col = col_mapping['problem_id']
	correct_col = col_mapping['correct']

	user_seq_dict = {}
	user_seq_dict.set_default()

	return

	for row in csv_reader:
		user = row[user_col]
		seq = row[seq_col]
		problem = row[problem_col]
		correc = row[correct_col]

		this_user = user_seq_dict.get(user)
		this_user_seq = this_user[seq]




if __name__ == "__main__":
	col_mapping = {'user_id': 1, 'sequence_id' : 2, 'problem_id' : 3, 'correct': 4}

	generate_PFA_data('../data/sql_data.csv', '../data/pfa_data.csv', col_mapping, 1)