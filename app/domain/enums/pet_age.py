from enum import Enum


class PetAge(str, Enum):
    BABY = "baby"
    YOUNG = "young"
    ADULT = "adult"
    SENIOR = "senior"
