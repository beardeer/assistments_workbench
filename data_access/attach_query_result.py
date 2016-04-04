# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 21:11:31 2015

@author: xxiong
"""

import assistments_workbench.data_access.db_access.general as dr
import assistments_workbench.data_access.db_access.ARRS as dr_arrs
import assistments_workbench.data_access.db_access.supporting_func as dr_supt
import csv
from copy import copy
from tqdm import tqdm

support_header = \
{
    # tuple(['sequence_id']):
    #     {
    #     'sequence_difficulty': dr.problem_set_difficulty
    #     },

    tuple(['problem_id']):
        {
        'problem_difficulty': dr.problem_difficulty
        },

    # tuple(['user_id']):
    #     {
    #     'user_reassessment_performance': dr_arrs.user_reassessment_performance,
    #     'user_all_class_assignment_performance':
    #         dr.user_all_class_assignment_performance,
    #     'user_all_homework_completion_rate': dr.user_all_homework_completion_rate
    #     },

    # tuple(['mastery_speed']):
    #     {
    #     'mastery_speed_bin': dr_supt.mastery_speed_bin
    #     },

    # ('user_id', 'class_assignment_id'):
    #     {
    #     'user_assignment_performance': dr.user_assignment_performance,
    #     'user_assignemnt_correct_num': dr.user_assignemnt_correct_num,
    #     'user_assignemnt_incorrect_num': dr.user_assignemnt_incorrect_num,
    #     'user_assignment_bottom_hint_num': dr.user_assignment_bottom_hint_num,
    #     'mastery_speed':
    #         dr.mastery_speed
    #     }
}


def attach_query_result_by_header(input_path, output_path = None):
    if output_path is None:
        output_path = input_path.split('.')[0] + '_w_feature.' + input_path.split('.')[1]
    input_file = open(input_path, 'rb')
    output_file = open(output_path, 'wb')
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    cache = {}
    header = reader.next()
    header = [i.lower() for i in header]
    header_idx_dict = {}
    for i, h in enumerate(header):
        header_idx_dict[h] = i
    # find which headers are in the input file
    contained_header = [h for h in support_header.keys()
                        if set(h).issubset(set(header))]
    # contained_header_idx = [header.index(h) for h in contained_header]
    # create new headers for output file
    new_header = copy(header)
    for h in contained_header:
        new_header.extend(support_header[h].keys())

    print 'contained header: ', contained_header
    print 'new header: ', new_header

    # initial cache
    for h in contained_header:
        for k in support_header[h].keys():
            cache[k] = {}

    writer.writerow(new_header)
    csv_data = [row for row in reader]

    print 'Running queries to attach new information ...'
    for row in tqdm(csv_data):
        new_row = copy(row)
        for h in contained_header:
            input_args = __build_input_args(row, h, header_idx_dict)
            for new_header, query in support_header[h].items():
                cache_keys = tuple(input_args.values())
                if cache_keys not in cache[new_header].keys():
                    cache[new_header][cache_keys] = query(**input_args)
                new_row.append(cache[new_header][cache_keys])
        writer.writerow(new_row)

    input_file.close()
    output_file.close()

    return output_path


def __build_input_args(row, input_headers, header_idx_dict):
    output = {}
    for h in input_headers:
        output[h] = row[header_idx_dict[h]]
    return output

if __name__ == "__main__":
    pass
    # input_location = r'data/arrs.csv'
    # output_location = r'data/arrs_with_feature.csv'

    # attach_query_result_by_header(input_location, output_location)
