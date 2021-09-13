from typing import Iterable
import random

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import Book

def get_languages(repo: AbstractRepository):
    languages = repo.get_languages()
    return languages