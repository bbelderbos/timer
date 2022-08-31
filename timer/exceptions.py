class DuplicateTimerException(Exception):
    """
    This exception is raised when a timer is launched
    for an activity that has not been ended.
    """
