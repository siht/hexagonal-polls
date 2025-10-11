# use_cases.py

# como ven nos faltan los test de integración para esta logica de negocio
from zope.interface import implementer

from .dtos import (
    ChoiceDTO,
    QuestionDTO,
)
from .exceptions import ChoiceNotFound
from .interfaces import (
    IChoiceRepository,
    ICreateChoiceExecutor,
    ICreateQuestionExecutor,
    IQuestionRepository,
    IVoteExecutor,
)

__all__ = (
    'CreateChoice',
    'CreateQuestion',
    'Vote',
)

@implementer(ICreateQuestionExecutor)
class CreateQuestion:
    def __init__(self, service=None): # se agrega service por si es neceasrio hace una inyección, pero no se usa
        self.question_repository = IQuestionRepository(self)

    def create(self, question: QuestionDTO) -> QuestionDTO:
        return self.question_repository.create(question)

    def execute(self, question: QuestionDTO) -> QuestionDTO:
        return self.create(question)


@implementer(ICreateChoiceExecutor)
class CreateChoice:
    def __init__(self, service = None): # se agrega service por si es neceasrio hace una inyección, pero no se usa
        self.choice_repository = IChoiceRepository(self)

    def create(self, choice_data: ChoiceDTO) -> ChoiceDTO:
        return self.choice_repository.create(choice_data)

    def execute(self, choice_data: ChoiceDTO) -> ChoiceDTO:
        return self.create(choice_data)


@implementer(IVoteExecutor)
class Vote:
    def __init__(self, service = None): # se agrega service por si es neceasrio hace una inyección, pero no se usa
        self.choice_repository = IChoiceRepository(self)

    def vote(self, choice_id: int) -> int:
        return self.choice_repository.vote(choice_id)

    def get_updated_choie(self, choice_id: int) -> ChoiceDTO:
        return self.choice_repository.get_by_id(choice_id)

    def execute(self, choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        self.vote(choice_id)
        choice = self.get_updated_choie(choice_id)
        return choice
