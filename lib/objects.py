from dataclasses import dataclass, field
from typing import List, Set
import ast

from lib.chatlib import DATA_DELIMITER


@dataclass
class User:
    username: str = field(compare=True, hash=True)
    password: str = field(compare=False, hash=False)
    score: int = field(default=0, compare=False, hash=False)
    questions_asked: Set[int] = field(default_factory=set, compare=False, hash=False)

    def format_for_save(self) -> str:
        return f"{self.username}|{self.password}|{self.score}|{self.questions_asked if len(self.questions_asked) != 0 else ''}"

    @staticmethod
    def parse_from_save(line: str) -> "User":
        user_info = line.split("|")
        username = user_info[0]
        password = user_info[1]
        score = int(user_info[2])
        if user_info[3] == "\n":
            questions_asked = set()
        else:
            questions_asked = ast.literal_eval(user_info[3])
        return User(username, password, score, questions_asked)


@dataclass
class Question:
    question_id: int = field(compare=True, hash=True)
    question: str = field(compare=False, hash=False)
    answers: List[str] = field(compare=False, hash=False)
    correct: int = field(compare=False, hash=False)

    def format_to_send(self) -> str:
        return f"{self.question_id}{DATA_DELIMITER}{self.question}{DATA_DELIMITER}{DATA_DELIMITER.join(self.answers)}"

    def format_for_save(self) -> str:
        return f"{self.question_id}|{self.question}|{self.answers}|{self.correct}"

    @staticmethod
    def parse_from_save(line: str) -> "Question":
        question_info = line.split("|")
        question_id = int(question_info[0])
        question = question_info[1]
        answers = ast.literal_eval(question_info[2])
        correct = int(question_info[3])
        return Question(question_id, question, answers, correct)
