from typing import Dict, List

from lib.objects import User, Question

path_to_db_folder = "../ongoing_mission/db"


# ~~ Users ~~ #

def read_users_from_file() -> List[str]:
    """
    Helper function to read all users from the file.
    """
    with open(path_to_db_folder + "/users.txt", "r") as f:
        return f.readlines()


def get_all_users() -> Dict[str, User]:
    """
    Returns all users in the file.
    It's return as a dictionary, where the key is the username and the value is the User object.
    :return:
    """
    return {user.username: user for user in
            [User.parse_from_save(line) for line in read_users_from_file()]}


def is_user_exists(username: str) -> bool:
    """
    Checks if the user exists in the file.
    :param username:
    :return:
    """
    return any([username == User.parse_from_save(line).username for line in read_users_from_file()])


def save_user(user: User) -> bool:
    """
    Saves user to the file.
    :param user:
    :return: True if the user was saved, False otherwise.
    """
    if is_user_exists(user.username):
        return False
    with open(path_to_db_folder + "/users.txt", "a+") as f:
        f.write(user.format_for_save() + "\n")
        return True


def update_data(user: User) -> bool:
    """
    Updates user data in the file.
    :param user:
    :return: True if user exists, False otherwise.
    """
    flag = False
    users_as_lines = read_users_from_file()
    with open(path_to_db_folder + "/users.txt", "w") as f:
        for line in users_as_lines:
            if user.username == User.parse_from_save(line).username:
                f.write(user.format_for_save() + "\n")
                flag = True
            else:
                f.write(line)

    return flag


# ~~ Questions ~~ #
def read_questions_from_file() -> List[str]:
    """
    Helper function to read all questions from the file.
    """
    with open(path_to_db_folder + "/questions.txt", "r") as f:
        return f.readlines()


def get_all_questions() -> Dict[int, Question]:
    """
    Returns all questions in the file.
    It's return as a dictionary, where the key is the question_id and the value is the question.
    :return:
    """
    return {question.question_id: question for question in
            [Question.parse_from_save(line) for line in read_questions_from_file()]}


def is_question_exists(question_id: int) -> bool:
    """
    Checks if the question exists in the file.
    :param question_id:
    :return:
    """
    return any([question_id == Question.parse_from_save(line).question_id for line in read_questions_from_file()])


def save_question(question: Question) -> bool:
    """
    Saves question to the file.
    :param question:
    :return: True if the question was saved, False otherwise.
    """
    if is_question_exists(question.question_id):
        return False
    with open(path_to_db_folder + "/questions.txt", "a+") as f:
        f.write(question.format_for_save() + "\n")
        return True


save_question(Question(2313, "How much is 2+2", ["3", "4", "2", "1"], 2),)
save_question(Question(4122, "What is the capital of France?", ["Lion", "Marseille", "Paris", "Montpelier"], 3),)
