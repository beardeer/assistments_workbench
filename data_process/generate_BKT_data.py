import csv
from math import ceil

from tqdm import tqdm

from data_converter import DataConverter

class BKTConverter(DataConverter):

	def convert(self):

		input_file = open(self.input_file_path, 'rb')
		csv_reader = csv.reader(input_file)


		header = csv_reader.next()

		user_col = self.col_mapping['user_id']
		seq_col = self.col_mapping['sequence_id']
		problem_col = self.col_mapping['problem_id']
		correct_col = self.col_mapping['correct']

		seq_user_dict = {}
		seq_list = []

		for row in csv_reader:
			user = row[user_col]
			seq = row[seq_col]
			problem = row[problem_col]
			correct = ceil(float(row[correct_col]))


			if seq_user_dict.has_key(seq) == False:
				seq_user_dict[seq] = {}
			this_seq = seq_user_dict.get(seq)

			if this_seq.has_key(user) == False:
				this_seq[user] = []
			this_seq_user = this_seq[user]

			this_seq_user.append(correct)

		input_file.close()

		for seq_id in tqdm(seq_user_dict.keys()):
			output_file_path = self.output_file_path.replace('nnn', seq_id)
			output_file = open(output_file_path, 'wb')
			csv_writer = csv.writer(output_file, delimiter='\t')

			users = seq_user_dict[seq_id]

			for user_id in users.keys():
				n = 0
				data = users[user_id]
				for d in data:
					n += 1
					csv_writer.writerow([user_id, int(d), n])

			output_file.close()


if __name__ == "__main__":
	col_mapping = {'user_id': 1, 'sequence_id' : 2, 'problem_id' : 3, 'correct': 4}

	converter = BKTConverter('../data/sql_data.csv', '../data/bkt/skill_nnn.csv', col_mapping)

	converter.convert()

