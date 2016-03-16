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

from connector import db, session
from supporting_func import get_performance, get_difficulty


now = datetime.now()


# ==============================================================================
#  main functions
# ==============================================================================


# id mapping


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

def valid_student_num_after_date(date_after = now):
    table = db.assignment_logs
    return table.filter(table.start_time > date_after).distinct(table.user_id).count()

# schools and classes

def class_num():
    return class_num_after_date(date_after = now)

def class_num_after_date(date_after = now):
    """Summary

    Returns:
        TYPE: Description
    """
    table = db.student_classes
    return table.filter(table.created_at > date_after).count()


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
    correct = table.filter(table.correct == 1,
        table.original == 1,
        table.problem_id == problem_id).count()
    incorrect = table.filter(table.correct < 1,
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


if __name__ == "__main__":
    import datetime

    print datetime.datetime.now()
    print user_all_class_assignment_performance(336579)
    print problem_difficulty(163430)
    print problem_set_difficulty(11833)
