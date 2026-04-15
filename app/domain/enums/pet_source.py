from enum import Enum


class PetSource(str, Enum):
    LOCAL = "local"
    EXTERNAL = "external"
