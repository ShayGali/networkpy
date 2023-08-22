from dataclasses import dataclass, field
from typing import List

from lib.chatlib import DATA_DELIMITER


@dataclass
class User:
    user_id: int = field(compare=True, hash=True)
    username: str = field(compare=False, hash=False)
    password: str = field(compare=False, hash=False)
    score: int = field(default=0, compare=False, hash=False)
    questions_asked: List[int] = field(default_factory=list, compare=False, hash=False)


@dataclass
class Question:
    question_id: int = field(compare=True, hash=True)
    question: str = field(compare=False, hash=False)
    answers: List[str] = field(compare=False, hash=False)
    correct: int = field(compare=False, hash=False)

    def format_to_send(self) -> str:
        return f"{self.question_id}{DATA_DELIMITER}{self.question}{DATA_DELIMITER}{DATA_DELIMITER.join(self.answers)}"
