from sharpy.plans.require import *
from sharpy.plans.terran import *
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sharpy.knowledges import KnowledgeBot

from sc2 import UnitTypeId


class BuildMech(BuildOrder):
    def __init__(self):

        scv = [
            Step(None, MorphOrbitals(),
                 skip_until=UnitExists(UnitTypeId.BARRACKS, 1)),
        ]

        opener = [
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 1, priority=True),
            BuildGas(1),
            GridBuilding(UnitTypeId.BARRACKS, 1),
            BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1),
            GridBuilding(UnitTypeId.FACTORY, 1),
            PlanAddonSwap(factory_techlab_count=1),
            Step(None, ExecuteAddonSwap(),
                 skip_until=UnitReady(UnitTypeId.FACTORY, 1)),
            GridBuilding(UnitTypeId.FACTORY, 2),
        ]

        super().__init__([AutoWorker(), AutoDepot(), scv, opener])


class Mechanic(KnowledgeBot):
    def __init__(self):
        super().__init__("TerranBot")

    async def create_plan(self) -> BuildOrder:
        tactics = [
            # Lower Depots, Repair, distribute SCVs, continue building
            LowerDepots(),
            Repair(),
            DistributeWorkers(),
            ContinueBuilding(),

            # Scout
            Step(
                None, WorkerScout(),
                skip_until=UnitExists(UnitTypeId.SUPPLYDEPOT, 1)
            ),

            # Call Mule, Scan enemy
            Step(None, CallMule(50), skip=Time(3 * 60)),
            Step(None, CallMule(100), skip_until=Time(3 * 60)),
            Step(None, ScanEnemy(), skip_until=Time(3 * 60)),

            # Cancel building
            PlanCancelBuilding(),

            # Distribute SCVs, lower Depots
            DistributeWorkers(),
            LowerDepots(),

            # Gather and Defend
            PlanZoneGatherTerran(),
            PlanZoneDefense(),

            # Attack and Finish the enemy
            PlanZoneAttack(5,),
            PlanFinishEnemy(),
        ]

        return BuildOrder([BuildMech(), SequentialList(tactics)])
