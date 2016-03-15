
from sqlalchemy import or_, and_, distinct, func

from connector import db, session
from supporting_func import get_performance, get_difficulty


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

