
import csv
from math import ceil
from tqdm import tqdm

from assistments_workbench.data_reader import problem_difficulty
from utility_dot_py.utility import DataCache


def generate_PFA_data(input_file_path, output_file_path, col_mapping = {}, pfa_model = 1):
	"""Summary

	Args:
	    input_file_path (TYPE): Description
	    output_file_path (TYPE): Description
	    col_mapping (dict, optional): Description
	    pfa_model (int, optional): Description

	Returns:
	    TYPE: Description
	"""
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
	difficulty_col = col_mapping.get('difficulty', -1)

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

		if difficulty_col != -1:
			difficulty = float(row[difficulty_col])
		else:
			difficulty = data_cache.get(problem)

		correct_num_list = [0] * len(seq_list)
		seq_pos = seq_list.index(seq)

		this_user = user_seq_dict.setdefault(user, {})

		this_user_seq = this_user.setdefault(seq, {'correct_num' : 0, 'incorrect_num' : 0})

		if pfa_model == 1:
			correct_num_list[seq_pos] = this_user_seq['correct_num']
			correct_num_list[seq_len + seq_pos] = this_user_seq['incorrect_num']
		elif pfa_model == 2:
			correct_num_list = [this_user_seq['correct_num'], this_user_seq['incorrect_num']]

		output_data = [correct, seq, user, difficulty] + correct_num_list

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
	col_mapping = {'user_id': 0, 'sequence_id' : 2, 'problem_id' : 1, 'correct': 3, 'difficulty': 6}

	col_mapping_2 = {'user_id': 1, 'sequence_id' : 6, 'problem_id' : 2, 'correct': 4}

	generate_PFA_data('../data/0910_no_dup.csv', '../data/0910_no_dup_PFA.csv', col_mapping, 2)
