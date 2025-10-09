# exceptions.py
class RepositoryError(Exception):
    """Excepción base para todos los errores relacionados con el repositorio."""
    ...


class EntityNotFound(RepositoryError):
    """
    Se lanza cuando una Entidad con el ID especificado no puede ser encontrado.
    """
    def __init__(self, message: str):
        super().__init__(message)


class QuestionNotFound(EntityNotFound):
    """
    Se lanza cuando un Question con el ID especificado no puede ser encontrado.
    """
    def __init__(self, message: str):
        super().__init__(message)


class ModelError(Exception):
    """Excepción base para errores de llenado en el modelo"""
    ...


class ChoiceDataError(ModelError):
    """Se lanza cuando hay inconsistencia de datos"""
    ...


class ChoiceNotFound(RepositoryError):
    """
    Se lanza cuando un Choice con el ID especificado no puede ser encontrado.
    """
    def __init__(self, message: str):
        super().__init__(message)
