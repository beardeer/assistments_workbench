# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 21:33:47 2015

@author: xxiong

Attributes:
    db (TYPE): Description
    db_str (TYPE): Description
    password (TYPE): Description
    session (TYPE): Description
    username (TYPE): Description
"""

from datetime import datetime

import sqlsoup
from sqlalchemy import or_, and_, distinct, func

from assistments_workbench.config_reader import config

username = config.get('postgres', 'username')
password = config.get('postgres', 'password')
db_url = config.get('postgres', 'db_url')

db_str = 'postgresql://%s:%s@%s/assistment_production' % \
    (username, password, db_url)

db = sqlsoup.SQLSoup(db_str)
session = db.session


# ==============================================================================
#  main functions
# ==============================================================================


# id mapping


def user_id_to_student_id(user_id):
    """Summary

    Args:
        user_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.user_roles
    return table.filter(table.user_id == user_id,
                        table.role_id == 4).one().id


def student_id_to_user_id(student_id):
    """Summary

    Args:
        student_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.user_roles
    return table.filter(table.id == student_id,
                        table.role_id == 4).one().user_id


# users
def total_user_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.users.count()


def student_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return user_num_by_role_id(4)


def teacher_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return user_num_by_role_id(2)


def parent_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return user_num_by_role_id(7)


# schools and classes


def class_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.student_classes.count()


def school_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.schools.count()


def enabled_class_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.student_classes.filter(db.student_classes.enabled == True).count()

# class_assignments


def total_class_assignment_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.class_assignments.count()


def class_assignment_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return class_assignment_num_by_assignment_type_id(1)

def relearning_assignment_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return class_assignment_num_by_assignment_type_id(6)


def reassessment_assignment_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return class_assignment_num_by_assignment_type_id(7)


# problems and problem_sets


def total_probelm_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.problems.count()


def main_probelm_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.assistments.count()


def total_problem_set_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.sequences.count()


def skill_builder_problem_set_num():
    """Summary

    Returns:
        TYPE: Description
    """
    sequences = db.sequences
    sections = db.with_labels(db.sections)
    join = db.join(sequences, sections,
                   sequences.head_section_id == sections.sections_id)
    where = sections.sections_type == 'MasterySection'
    result = join.filter(where).count()
    return result


# probelm_logs


def problem_log_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.problem_logs.count()


def main_problem_log_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.problem_logs.filter(db.problem_logs.original == 1).count()


def mastery_speed(user_id, class_assignment_id):
    """Summary

    Args:
        user_id (TYPE): Description
        class_assignment_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.problem_logs
    return table.filter(table.user_id == user_id,
                        table.assignment_id == class_assignment_id,
                        table.original == 1).count()


def user_assignemnt_correct_num(user_id, class_assignment_id):
    """Summary

    Args:
        user_id (TYPE): Description
        class_assignment_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.problem_logs
    return table.filter(table.user_id == user_id,
                        table.assignment_id == class_assignment_id,
                        table.original == 1,
                        table.correct == 1).count()


def user_assignemnt_incorrect_num(user_id, class_assignment_id):
    """Summary

    Args:
        user_id (TYPE): Description
        class_assignment_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.problem_logs
    return table.filter(table.user_id == user_id,
                        table.assignment_id == class_assignment_id,
                        table.original == 1,
                        table.correct < 1).count()


def user_assignment_performance(user_id, class_assignment_id):
    """Summary

    Args:
        user_id (TYPE): Description
        class_assignment_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    correct = user_assignemnt_correct_num(user_id, class_assignment_id)
    incorrect = user_assignemnt_incorrect_num(user_id, class_assignment_id)
    return get_performance(correct, incorrect)


def user_assignment_bottom_hint_num(user_id, class_assignment_id):
    """Summary

    Args:
        user_id (TYPE): Description
        class_assignment_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.problem_logs
    return table.filter(table.user_id == user_id,
                        table.assignment_id == class_assignment_id,
                        table.original == 1,
                        table.bottom_hint == 1).count()
# performance_data


def all_problem_difficulty():
    """Summary

    Returns:
        TYPE: Description
    """
    correct = db.problem_logs.filter(db.problem_logs.correct == 1).count()
    incorrect = db.problem_logs.filter(db.problem_logs.correct < 1).count()
    return get_difficulty(correct, incorrect)


def main_problem_difficulty():
    """Summary

    Returns:
        TYPE: Description
    """
    correct = db.problem_logs.filter(db.problem_logs.correct == 1,
                                     db.problem_logs.original == 1).count()
    incorrect = db.problem_logs.filter(db.problem_logs.correct < 1,
                                       db.problem_logs.original == 1).count()
    return get_difficulty(correct, incorrect)


def problem_difficulty(problem_id):
    """Summary

    Args:
        problem_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = db.problem_logs
    correct = db.problem_logs.filter(table.correct == 1,
                                     table.original == 1,
                                     table.problem_id == problem_id).count()
    incorrect = db.problem_logs.filter(table.correct < 1,
                                       table.original == 1,
                                       table.problem_id == problem_id).count()
    return get_difficulty(correct, incorrect)


def problem_set_difficulty(sequence_id):
    """Summary

    Args:
        sequence_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    class_assignments = db.class_assignments
    problem_logs = db.with_labels(db.problem_logs)
    join = db.join(class_assignments, problem_logs,
                   class_assignments.id ==
                   problem_logs.problem_logs_assignment_id)
    where = and_(problem_logs.problem_logs_original == 1,
                 class_assignments.sequence_id == sequence_id)
    correct = join.filter(where,
                          problem_logs.problem_logs_correct == 1).count()
    incorrect = join.filter(where,
                            problem_logs.problem_logs_correct < 1).count()
    return get_difficulty(correct, incorrect)


def user_all_class_assignment_performance(user_id):
    """Summary

    Args:
        user_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    problem_logs = db.problem_logs
    class_assignments = db.with_labels(db.class_assignments)
    join = db.join(class_assignments, problem_logs,
                   problem_logs.assignment_id ==
                   class_assignments.class_assignments_id)
    correct = join.filter(class_assignments.class_assignments_assignment_type_id == 1,
                          problem_logs.correct == 1,
                          problem_logs.original == 1,
                          problem_logs.user_id == user_id).count()
    incorrect = join.filter(class_assignments.class_assignments_assignment_type_id == 1,
                            problem_logs.correct < 1,
                            problem_logs.original == 1,
                            problem_logs.user_id == user_id).count()
    return get_performance(correct, incorrect)


# assignment_log

def user_all_homework_completion_rate(user_id):
    """Summary

    Args:
        user_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    assignment_logs = db.assignment_logs
    class_assignments = db.with_labels(db.class_assignments)
    join = db.join(class_assignments, assignment_logs,
                   assignment_logs.assignment_id ==
                   class_assignments.class_assignments_id)
    complete = join.filter(class_assignments.class_assignments_assignment_type_id == 1,
                           assignment_logs.user_id == user_id,
                           assignment_logs.end_time != None).count()
    incomplete = join.filter(class_assignments.class_assignments_assignment_type_id == 1,
                             assignment_logs.user_id == user_id,
                             assignment_logs.end_time == None).count()
    return get_performance(complete, incomplete)

# arrs data


def arrs_record_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.student_reassessment_records.count()


def reassessment_test_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.student_reassessment_tests.count()


def reassessment_problem_nums():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.student_reassessment_problems.count()


def relearning_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return db.student_relearning_records.count()


def arrs_class_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return session.query\
    (distinct(db.student_reassessment_records.student_class_id)).count()
    return db.student_reassessment_records.student_class_id


def arrs_enable_class_num():
    """Summary

    Returns:
        TYPE: Description
    """
    arrs = db.student_reassessment_records
    classes = db.with_labels(db.student_classes)
    join = db.join(arrs, classes,
                   arrs.student_class_id == classes.student_classes_id)
    where = classes.student_classes_enabled == True
    return join.filter(where).distinct(arrs.student_class_id).count()


def arrs_student_num():
    """Summary

    Returns:
        TYPE: Description
    """
    return session.query\
    (distinct(db.student_reassessment_records.student_id)).count()

def reassessment_problem_num_by_date(date_before):
    table = db.student_reassessment_problems
    return table.filter(table.release_date < date_before).count()


def relearning_assignment_num_by_date(date_before):
    table = db.student_relearning_records
    return table.filter(table.assign_date < date_before).count()


def user_reassessment_performance(user_id):
    """Summary

    Args:
        user_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    arrs = db.student_reassessment_problems
    problem_logs = db.with_labels(db.problem_logs)
    join = db.join(arrs, problem_logs,
                   arrs.problem_log_id == problem_logs.problem_logs_id)
    where = arrs.student_id == user_id_to_student_id(user_id)
    correct = join.filter(where,
                          problem_logs.problem_logs_correct == 1).count()
    incorrect = join.filter(where,
                            problem_logs.problem_logs_correct < 1).count()
    return get_performance(correct, incorrect)


# ==============================================================================
#  supporting functions
# ==============================================================================

def mastery_speed_bin(mastery_speed):
    """Summary

    Args:
        mastery_speed (TYPE): Description

    Returns:
        TYPE: Description
    """
    if mastery_speed < 3:
        return -1
    if 3 <= mastery_speed <= 4:
        return 1
    elif 5 <= mastery_speed <= 7:
        return 2
    else:
        return 3

def user_num_by_role_id(role_id):
    """Summary

    Args:
        role_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    return db.user_roles.filter(db.user_roles.role_id == role_id).count()


def class_assignment_num_by_assignment_type_id(type_id):
    """Summary

    Args:
        type_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    return db.class_assignments.filter\
        (db.class_assignments.assignment_type_id == type_id).count()


def get_performance(correct_num, incorrect_num):
    """Summary

    Args:
        correct_num (TYPE): Description
        incorrect_num (TYPE): Description

    Returns:
        TYPE: Description
    """
    if correct_num == 0 and incorrect_num == 0:
        return 0
    else:
        return float(correct_num) / (correct_num + incorrect_num)


def get_difficulty(correct_num, incorrect_num):
    """Summary

    Args:
        correct_num (TYPE): Description
        incorrect_num (TYPE): Description

    Returns:
        TYPE: Description
    """
    if correct_num == 0 and incorrect_num == 0:
        return 0
    else:
        return float(incorrect_num) / (correct_num + incorrect_num)

if __name__ == "__main__":
    import datetime

    print datetime.datetime.now()
    print user_all_class_assignment_performance(336579)
    print problem_difficulty(163430)
    print problem_set_difficulty(11833)
