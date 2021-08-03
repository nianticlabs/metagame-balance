from copy import deepcopy
from typing import List, Dict

from framework.DataObjects import DesignConstraints, Target, Rule, PkmTemplate, PkmRosterView, MetaData, \
    get_pkm_roster_view, PkmRoster


class VGCRule(Rule):

    def __init__(self, base_roster_view, target_template=None):
        self._base_roster_view = base_roster_view
        self._target_template = target_template

    def check(self, roster: PkmRosterView) -> bool:
        pass


class VGCTarget(Target):

    def check(self, meta_game: MetaData) -> bool:
        pass


class VGCDesignConstraints(DesignConstraints):

    def __init__(self, base_roster: PkmRoster):
        self._base_roster = deepcopy(base_roster)
        self._base_roster_view = get_pkm_roster_view(self._base_roster)
        self._allpkm_rule_set: List[VGCRule] = []
        self._pkm_rule_set: Dict[PkmTemplate, List[VGCRule]] = {}
        self._global_rule_set: List[VGCRule] = []
        self._target_set: List[VGCTarget] = []

    def get_base_roster(self) -> PkmRosterView:
        return self._base_roster_view

    def get_allpkm_rule_set(self) -> List[Rule]:
        return self._allpkm_rule_set

    def add_allpkm_rule(self, rule: VGCRule):
        self._allpkm_rule_set.append(rule)

    def get_pkm_rule_set(self, template: PkmTemplate) -> List[Rule]:
        return self._pkm_rule_set[template]

    def add_pkm_rule(self, template: PkmTemplate, rule: VGCRule):
        if template not in self._pkm_rule_set:
            self._pkm_rule_set[template] = []
        self._pkm_rule_set[template].append(rule)

    def get_global_rule_set(self) -> List[Rule]:
        return self._global_rule_set

    def add_global_rule(self, rule: VGCRule):
        self._global_rule_set.append(rule)

    def get_target_set(self) -> List[Target]:
        return self._target_set

    def add_target(self, target: VGCTarget):
        self._target_set.append(target)
