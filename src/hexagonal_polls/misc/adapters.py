from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from zope.interface import implementer

from ..dtos import (
    ChoiceDTO,
    QuestionDTO,
)

from ..exceptions import (
    ChoiceDataError,
    QuestionDataError,
) 
from ..use_cases import (
    IVoteExecutor,
    ICreateChoiceExecutor,
    ICreateQuestionExecutor,
)
from .helper_interfaces import (
    IVoteIOFrameworkAdapter,
    IChoiceCreatorIOFrameworkAdapter,
    IQuestionCreatorIOFrameworkAdapter,
)

__all__ = (
    'AbstractVoteIOFrameworkAdapter',
    'AbstractChoiceCreatorIOFrameworkAdapter',
    'AbstractQuestionCreatorIOFrameworkAdapter',
)

@implementer(IVoteIOFrameworkAdapter)
class AbstractVoteIOFrameworkAdapter(ABC):
    def __init__(self):
        self.vote_executor = IVoteExecutor(self)

    @abstractmethod
    def input(self, input: Any) -> int:
        """Return integer. Is the choice id"""
        ...

    @abstractmethod
    def output(self, choice: ChoiceDTO) -> Any:
        """Return something related with Choice. """
        ...

    def validate(self, choice_id: int) -> int:
        # pudiera buscarse primero el registro en db, pero no se hará
        # if not choice_id:
        #     raise ChoiceDataError('es necesario el campo question_id para la creacion de un Choice')
        return choice_id

    def execute(self, input: Any) -> Any:
        """Return something related with Choice"""
        id_choice = self.input(input)
        updated_choice = self.vote_executor.execute(id_choice)
        return self.output(updated_choice)


@implementer(IChoiceCreatorIOFrameworkAdapter)
class AbstractChoiceCreatorIOFrameworkAdapter(ABC):
    def __init__(self):
        self.choice_executor = ICreateChoiceExecutor(self)

    @abstractmethod
    def input(self, input: Any) -> ChoiceDTO:
        """Return integer. Is the choice id"""
        ...

    @abstractmethod
    def output(self, choice: ChoiceDTO) -> Any:
        """Return something related with Choice. """
        ...

    def validate(self, data: ChoiceDTO) -> ChoiceDTO:
        no_ingresaron_votos_iniciales = data.votes is None
        if no_ingresaron_votos_iniciales:
            data.votes = 0
        es_un_dto_para_creacion = not data.id and not data.question_id
        if es_un_dto_para_creacion:
            raise ChoiceDataError('es necesario el campo question_id para la creacion de un Choice')
        return data

    def execute(self, input: Any) -> Any:
        """Return something related with Choice"""
        choice = self.input(input)
        validated_choice = self.validate(choice)
        return self.output(self.choice_executor.execute(validated_choice))


@implementer(IQuestionCreatorIOFrameworkAdapter)
class AbstractQuestionCreatorIOFrameworkAdapter(ABC):
    def __init__(self):
        self.choice_executor = ICreateQuestionExecutor(self)

    @abstractmethod
    def input(self, input: Any) -> QuestionDTO:
        """Return Question. Is the choice id"""
        ...

    @abstractmethod
    def output(self, question: QuestionDTO) -> Any:
        """Return something related with Question. """
        ...

    def validate(self, data: QuestionDTO) -> QuestionDTO:
        es_un_dto_de_creacion = not data.id
        errors = []
        if es_un_dto_de_creacion:
            if not data.pub_date:
                errors.append('Para crear una pregunta debe tener fecha')
            if data.question_text:
                errors.append('Para crear una pregunta debe tener question_text')
        if errors:
            raise QuestionDataError(errors)
        return data

    def execute(self, input: Any) -> Any:
        """Return something related with Choice"""
        choice = self.input(input)
        validated_choice = self.validate(choice)
        saved_choice = self.choice_executor.execute(validated_choice)
        return self.output(saved_choice)
