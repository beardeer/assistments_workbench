
import csv
from math import ceil
from tqdm import tqdm

from assistments_workbench.data_reader import problem_difficulty
from utility_dot_py.utility import DataCache


def generate_PFA_data(input_file_path, output_file_path, col_mapping = {}, pfa_model = 1):
	input_file = open(input_file_path, 'rb')
	csv_reader = csv.reader(input_file)

	output_file = open(output_file_path, 'wb')
	csv_writer = csv.writer(output_file)

	header = csv_reader.next()

	data_cache = DataCache(problem_difficulty)

	user_col = col_mapping['user_id']
	seq_col = col_mapping['sequence_id']
	problem_col = col_mapping['problem_id']
	correct_col = col_mapping['correct']

	user_seq_dict = {}
	seq_list = []
	csv_data = []

	# for tqdm to work
	for row in tqdm(csv_reader):
		seq = row[seq_col]
		seq_list.append(seq)
		csv_data.append(row)

	seq_list = list(set(seq_list))
	seq_len = len(seq_list)
	seq_list.sort()
	seq_list = seq_list + seq_list

	for row in tqdm(csv_data):
		user = row[user_col]
		seq = row[seq_col]
		problem = row[problem_col]
		correct = ceil(float(row[correct_col]))
		
		correct_num_list = [0] * len(seq_list)
		seq_pos = seq_list.index(seq)

		if user_seq_dict.has_key(user) == False:
			user_seq_dict[user] = {}
		this_user = user_seq_dict.get(user)

		if this_user.has_key(seq) == False:
			this_user[seq] = {'correct_num' : 0, 'incorrect_num' : 0}
		this_user_seq = this_user[seq]

		difficulty = data_cache.get(problem)

		correct_num_list[seq_pos] = this_user_seq['correct_num']
		correct_num_list[seq_len + seq_pos] = this_user_seq['incorrect_num']

		output_data = [seq] + correct_num_list + [difficulty, correct]

		csv_writer.writerow(output_data)

		if correct == 1.0:
			this_user_seq['correct_num'] += 1
		else:
			this_user_seq['incorrect_num'] += 1
			correct = 0

	input_file.close()
	output_file.close()

	print len(output_data)


if __name__ == "__main__":
	col_mapping = {'user_id': 1, 'sequence_id' : 2, 'problem_id' : 3, 'correct': 4}

	generate_PFA_data('../data/sql_data.csv', '../data/pfa_data.csv', col_mapping, 1)