from connector import db, session

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
