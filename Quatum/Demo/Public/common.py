__all__ = ["check_or_none","check_list_all_int", "check_list_all_digit"]

def check_or_none(*args):
    """Check if the given arguments are not None"""
    if "" in args:
        return True
    return False

def check_list_all_int(check_list):
    for num in check_list:
        if not isinstance(num, int):
            return False
        return True

def check_list_all_digit(check_list):
    for num in check_list:
        if not str(num).isdigit():
            return False
        return True

if __name__ == "__main__":
    a = [1, 2, 3]
    print(check_list_all_digit(a))