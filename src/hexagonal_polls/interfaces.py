# interfaces.py

from typing import (
    Any,
    Dict,
    List,
    TypeVar,
    Union,
)

from zope.interface import Interface

from . exceptions import EntityNotFound
from .dtos import (
    ChoiceDTO,
    QuestionDTO,
)

__all__ = (
    'IChoiceRepository',
    'ICreateChoiceExecutor',
    'ICreateQuestionExecutor',
    'IExecuteVote',
    'IGetQuestionRecent',
    'IQuestionRepository',
    'IRepository',
    'IVoteExecutor',
)


Criteria = Dict[str, Any] 

T = TypeVar('T')


class IRepository(Interface): 
    """
    PUERTO REPOSITORIO GENÉRICO.
    Define el contrato CRUD (Crear, Leer, Actualizar, Borrar) para la persistencia 
    de cualquier Entidad de Dominio T, sin conocer la tecnología de base de datos.
    """
    
    def get_by_id(entity_id: int) -> Union[T, None, EntityNotFound]:
        """
        Busca y retorna la Entidad T por su identificador primario.
        
        :param entity_id: ID de la entidad a buscar.
        :return: La Entidad T si fue encontrada. Retorna None o lanza EntityNotFound 
                 si se quiere un contrato más estricto.
        """
        
    def get_all() -> List[T]:
        """
        Retorna una lista[T] de todas las entidades en el sistema de persistencia.
        
        :return: Una lista de entidades T.
        """

    def create(entity: T) -> T:
        """
        Crea una nueva Entidad T.
        
        :param entity: La Entidad T de Dominio a crear.
        :return: La Entidad T creada, incluyendo el ID asignado por la base de datos.
        """

    def update(entity: T) -> T | None:
        """
        Actualiza una Entidad T existente con la información proporcionada.
        
        :param entity: La Entidad T de Dominio con los datos actualizados (debe tener ID).
        :return: La Entidad T actualizada o None si no se encontró el ID para actualizar.
        """

    def delete(entity_id: int) -> None:
        """
        Elimina una Entidad del sistema de persistencia por su ID.
        
        :param entity_id: ID de la entidad a eliminar.
        """


class IGetQuestionRecent(Interface):
    def get_recent(limit: int=5) -> list[QuestionDTO]:
        """Return a list[QuestionDTO] limited by limit"""
        pass


class IExecuteVote(Interface):
    def update_votes(choice_id: int) -> int:
        """Return int the actual votes and update vote counter for an specific Choice."""


class IQuestionRepository(IRepository, IGetQuestionRecent):
    pass


class IChoiceRepository(IRepository, IExecuteVote):
    pass


class ICreateQuestionExecutor(Interface):
    def execute(question: QuestionDTO) -> QuestionDTO:
        """Return a QuestionDTO"""

    def create(question: QuestionDTO) -> QuestionDTO:
        """Return a QuestionDTO"""


class ICreateChoiceExecutor(Interface):
    def execute(choice_data: ChoiceDTO) -> ChoiceDTO:
        """Return a ChoiceDTO. create a new Choice"""

    def create(choice_data: ChoiceDTO) -> ChoiceDTO:
        """Return a ChoiceDTO. create a new Choice"""


class IVoteExecutor(Interface):
    def execute(choice_id: int) -> ChoiceDTO:
        """Return ChoiceDTO updated."""

    def vote(choice_id: int) -> int:
        """Return int the actual votes and update vote counter for an specific Choice."""
