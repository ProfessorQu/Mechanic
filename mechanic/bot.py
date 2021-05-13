from sharpy.plans.require import UnitExists
from sharpy.plans.terran import MorphOrbitals, GridBuilding, BuildGas,\
    BuildAddon, AutoWorker, AutoDepot, LowerDepots, Repair, DistributeWorkers,\
    ContinueBuilding, CallMule, WorkerScout, Time, ScanEnemy,\
    PlanCancelBuilding, PlanZoneGatherTerran, PlanZoneDefense, PlanZoneAttack,\
    PlanFinishEnemy, TerranUnit, Expand
from sharpy.plans import BuildOrder, Step, SequentialList
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
            GridBuilding(UnitTypeId.FACTORY, 1),
            BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 1),
            BuildGas(2),
            GridBuilding(UnitTypeId.STARPORT, 1),
            BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 1),
            Step(None, GridBuilding(UnitTypeId.FACTORY, 2),
                 skip_until=UnitExists(UnitTypeId.CYCLONE)),
            BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 2),
            Expand(1),
            BuildGas(4),
            GridBuilding(UnitTypeId.FACTORY, 3),
            BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 3),
        ]

        units = [
            BuildOrder(
                TerranUnit(UnitTypeId.MARINE, 10),
            ),
            BuildOrder(
                TerranUnit(UnitTypeId.CYCLONE, 2),
                TerranUnit(UnitTypeId.SIEGETANK, 4),
            ),
        ]

        super().__init__([AutoWorker(), AutoDepot(), scv, opener, units])


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
            PlanZoneAttack(),
            PlanFinishEnemy(),
        ]

        return BuildOrder([BuildMech(), SequentialList(tactics)])
