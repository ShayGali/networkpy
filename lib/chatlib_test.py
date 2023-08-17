from chatlib import *


def test_build_message() -> None:
    # Test 1
    cmd = "LOGIN"
    data = "username#password"
    res = build_message(cmd, data)
    expected = "LOGIN           |0017|username#password"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 2
    cmd = "LOGIN"
    data = "aaaabbbb"
    res = build_message(cmd, data)
    expected = "LOGIN           |0008|aaaabbbb"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 3
    cmd = "LOGIN"
    data = ""
    res = build_message(cmd, data)
    expected = "LOGIN           |0000|"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 4
    cmd = "01234566789ABCDEFGH"
    data = ""
    res = build_message(cmd, data)
    assert res is None, f'Expected: None but got {res}'

    # Test 5
    cmd = "LOGIN"
    data = "0" * (MAX_DATA_LENGTH + 1)
    res = build_message(cmd, data)
    assert res is None, f'Expected: None but got {res}'


def test_parse_message() -> None:
    # Test 1
    msg = "LOGIN           |0017|username#password"
    res = parse_message(msg)
    expected = ("LOGIN", "username#password")
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 2
    msg = "LOGIN           |0008|aaaabbbb"
    res = parse_message(msg)
    expected = ("LOGIN", "aaaabbbb")
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 3
    msg = "LOGIN           |8|aaaabbbb"
    res = parse_message(msg)
    expected = (None, None)
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 4
    msg = "LOGIN           $0008|aaaabbbb"
    res = parse_message(msg)
    expected = (None, None)
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 5
    msg = "LOGIN           |000z|aaaabbbb"
    res = parse_message(msg)
    expected = (None, None)
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 6
    msg = "LOGIN           |0008|123456789"
    res = parse_message(msg)
    expected = (None, None)
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 7
    msg = "LOGIN|0008|aaaabbbb"
    res = parse_message(msg)
    expected = (None, None)
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 8
    msg = "                |0008|aaaabbbb"
    res = parse_message(msg)
    expected = ("", "aaaabbbb")
    assert res == expected, f'Expected: {expected} but got {res}'


def test_join_data() -> None:
    """ Test the join_data function """
    # Test 1
    lst = ["cell1", "cell2", "cell3"]
    res = join_data(lst)
    expected = "cell1#cell2#cell3"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 2
    lst = ["1", "2", "3", "4"]
    res = join_data(lst)
    expected = "1#2#3#4"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 3 - with floating numbers
    lst = ["1.1", "2.2", "3.3", "4.4"]
    res = join_data(lst)
    expected = "1.1#2.2#3.3#4.4"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 4
    lst = ["username", "password"]
    res = join_data(lst)
    expected = "username#password"
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 5
    lst = ["question", "ans1", "ans2", "ans3", "ans4", "correct"]
    res = join_data(lst)
    expected = "question#ans1#ans2#ans3#ans4#correct"
    assert res == expected, f'Expected: {expected} but got {res}'


def test_split_data() -> None:
    # Test 1
    msg = "cell1#cell2#cell3"
    res = split_data(msg, 3)
    expected = ["cell1", "cell2", "cell3"]
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 2
    msg = "username#password"
    res = split_data(msg, 2)
    expected = ["username", "password"]
    assert res == expected, f'Expected: {expected} but got {res}'

    # Test 3
    msg = "username#password"
    res = split_data(msg, 1)
    assert res is None, f'Expected: None but got {res}'

    # Test 4
    msg = "username"
    res = split_data(msg, 2)
    assert res is None, f'Expected: None but got {res}'


def their_tests() -> None:
    def check_build(input_cmd, input_data, expected_output):
        print("Input: ", input_cmd, input_data, "\nExpected output: ", expected_output)
        try:
            output = build_message(input_cmd, input_data)
        except Exception as e:
            output = "Exception raised: " + str(e)

        if output == expected_output:
            print(".....\t SUCCESS")
        else:
            print(".....\t FAILED, output: ", output)

    def check_parse(msg_str, expected_output):
        print("Input: ", msg_str, "\nExpected output: ", expected_output)

        try:
            output = parse_message(msg_str)
        except Exception as e:
            output = "Exception raised: " + str(e)

        if output == expected_output:
            print(".....\t SUCCESS")
        else:
            print(".....\t FAILED, output: ", output)

    # BUILD

    # Valid inputs
    # Normal message
    check_build("LOGIN", "aaaa#bbbb", "LOGIN           |0009|aaaa#bbbb")
    check_build("LOGIN", "aaaabbbb", "LOGIN           |0008|aaaabbbb")
    # Zero-length message
    check_build("LOGIN", "", "LOGIN           |0000|")

    # Invalid inputs
    # cmd too long
    check_build("0123456789ABCDEFG", "", None)
    # msg too long
    check_build("A", "A" * (MAX_DATA_LENGTH + 1), None)

    # PARSE

    # Valid inputs
    check_parse("LOGIN           |0009|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    check_parse(" LOGIN          |0009|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    check_parse("           LOGIN|0009|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    check_parse("LOGIN           |0009|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
    check_parse("LOGIN           |0004|data", ("LOGIN", "data"))

    # Invalid inputs
    check_parse("", (None, None))
    check_parse("LOGIN           x	  4|data", (None, None))
    check_parse("LOGIN           |	  4xdata", (None, None))
    check_parse("LOGIN           |	 -4|data", (None, None))
    check_parse("LOGIN           |	  z|data", (None, None))
    check_parse("LOGIN           |	  5|data", (None, None))


if __name__ == '__main__':
    GREEN_COLOR = "\033[32m"
    DEFAULT_COLOR = "\033[0m"

    test_build_message()
    test_parse_message()
    test_split_data()
    test_join_data()

    their_tests()

    print(f'{GREEN_COLOR}All tests passed!{DEFAULT_COLOR}')
