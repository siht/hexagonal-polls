# dtos.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = (
    'QuestionDTO',
    'ChoiceDTO',
)


@dataclass
class QuestionDTO:
    """Entidad de dominio - solo datos, sin lógica"""
    question_text: str
    id: Optional[int] = None
    pub_date: Optional[datetime] = None


@dataclass
class ChoiceDTO:
    """Entidad de dominio - solo datos, sin lógica"""
    text: str
    question_id: Optional[int] = None
    id: Optional[int] = None
    votes: Optional[int] = None
