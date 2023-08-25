__all__ =["check_or_none"]

def check_or_none(*args):
    """Check if the given arguments are not None"""
    if "" in args:
        return True
    return False

