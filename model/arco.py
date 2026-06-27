from dataclasses import dataclass

from model.team import Team


@dataclass
class Arco:
    t1: Team
    t2: Team
    peso: int