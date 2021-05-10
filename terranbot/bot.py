from sharpy.plans.acts import *
from sharpy.plans.acts.terran import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.plans.tactics.terran import *
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.knowledges import KnowledgeBot
from sc2 import UnitTypeId
import random


class TerranBot(KnowledgeBot):
    def __init__(self):
        super().__init__("TerranBot")

    async def pre_step_execute(self):
        pass

    async def create_plan(self) -> BuildOrder:
        return BuildOrder([
            Step(None, GridBuilding(UnitTypeId.SUPPLYDEPOT, 10)),
            Step(None, ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 10)),
            Expand(1),
            LowerDepots(),
        ])
