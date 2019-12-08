from math import log


def is_valid_password(password: int) -> bool:
    """
    Is the password given as input is valid ?
    """
    # Is a six digit number
    if int(log(password, 10)) + 1 != 6:
        return False

    # Two adjacent digits are the same
    # AND
    # strictly increasing number
    txt_num = str(password)
    condition_valid = False
    for i in range(5):
        if txt_num[i] == txt_num[i + 1]:
            condition_valid = True
        if txt_num[i] > txt_num[i + 1]:
            condition_valid = False
            break
    if not condition_valid:
        return False

    return True


def is_valid_password_2(password: int) -> bool:
    """
    Is the password given as input is valid ?
    """
    # Is a six digit number
    if int(log(password, 10)) + 1 != 6:
        return False

    # Two adjacent digits are the same BUT not part of a larger group
    # AND
    # strictly increasing number
    txt_num = str(password)
    condition_valid = False
    for i in range(5):
        if txt_num[i] == txt_num[i + 1]:
            if i > 0:
                if txt_num[i - 1] != txt_num[i]:
                    if i < 4:
                        if txt_num[i] != txt_num[i + 2]:
                            condition_valid = True
                    else:
                        condition_valid = True
            elif txt_num[i + 2] != txt_num[i]:
                    condition_valid = True
        if txt_num[i] > txt_num[i + 1]:
            condition_valid = False
            break
    if not condition_valid:
        return False

    return True


def generate_password(range_password: list, valid_password) -> list:
    """
        Generate a list of password that satisfy a specific condition
    """
    possible_passwords = []
    for tmp_password in range(range_password[0], range_password[1] + 1):
        if valid_password(tmp_password):
            possible_passwords.append(tmp_password)

    return possible_passwords


if __name__ == '__main__':
    with open("input.csv", mode='r') as input_file:
        range_password = [int(x) for x in input_file.read().split("-")]

        assert is_valid_password(111111)
        assert not is_valid_password(223450)
        assert not is_valid_password(123789)

        print(
            "Answer #4.1: ",
            len(generate_password(range_password, is_valid_password))
        )

        assert not is_valid_password_2(111111)
        assert is_valid_password_2(112233)
        assert not is_valid_password_2(123444)
        assert is_valid_password_2(111122)
        assert not is_valid_password_2(111456)

        assert not is_valid_password_2(122234)
        assert not is_valid_password_2(123334)
        assert not is_valid_password_2(123444)

        print(
            "Answer #4.2: ",
            len(generate_password(range_password, is_valid_password_2))
        )
