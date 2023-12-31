# Protocol Constants
from typing import List, Tuple, Union

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_login_players": "LOGGED",
    "get_question": "GET_QUESTION",
    "send_answer": "SEND_ANSWER",
    "get_score_msg": "MY_SCORE",
    "get_high_score_msg": "HIGHSCORE",
}

PROTOCOL_SERVER = {
    "error_msg": "ERROR",
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "LOGIN_FAILED",
    "get_login_players_msg": "LOGGED_ANSWER",
    "get_question": "YOUR_QUESTION",
    "correct_answer": "CORRECT_ANSWER",
    "wrong_answer": "WRONG_ANSWER",
    "get_score_msg": "YOUR_SCORE",
    "get_high_score_msg": "ALL_SCORE",
    "no_questions": "NO_QUESTIONS",
}


def build_message(cmd: str, data: str) -> Union[str, None]:
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occurred
    """
    if cmd not in PROTOCOL_SERVER.values() and cmd not in PROTOCOL_CLIENT.values():
        return None

    if len(data) > MAX_DATA_LENGTH:
        return None

    cmd_part = f'{cmd}{" " * (CMD_FIELD_LENGTH - len(cmd))}'
    data_len_part = str(len(data)).zfill(LENGTH_FIELD_LENGTH)

    return f'{cmd_part}|{data_len_part}|{data}'


def parse_message(data: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
    """
    if data is None or len(data) > MAX_MSG_LENGTH:
        return None, None

    split_msg_by_delimiter = data.split(DELIMITER)

    # check if the message has 3 parts
    if len(split_msg_by_delimiter) != 3:
        return None, None

    # check if we get a valid length of cmd
    if len(split_msg_by_delimiter[0]) != CMD_FIELD_LENGTH:
        return None, None

    # remove white spaces from cmd
    cleaned_cmd = split_msg_by_delimiter[0].replace(" ", "")

    data_length = split_msg_by_delimiter[1]

    # check if the length is 4 digits
    if len(data_length) != 4 or not data_length.isdigit():
        return None, None

    data_length = int(data_length)  # convert to string to int to get only the number
    data = split_msg_by_delimiter[2]  # get the data part of the message

    # check if all the data has been received
    if data_length != len(data):
        return None, None

    return cleaned_cmd, data


def split_data(msg: str, expected_fields: int) -> Union[List[str], None]:
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """

    if msg is None or msg.count(DATA_DELIMITER) != expected_fields - 1:
        return None

    return msg.split(DATA_DELIMITER)


def join_data(msg_fields: List[str]) -> str:
    """
    Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    return DATA_DELIMITER.join(msg_fields)
