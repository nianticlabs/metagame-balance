from abc import abstractmethod
from copy import deepcopy
from typing import List, Dict

from framework.DataObjects import DesignConstraints, Target, Rule, PkmTemplate, PkmRosterView, MetaData, \
    get_pkm_roster_view, PkmRoster, get_pkm_move_roster_view


class VGCRule(Rule):

    def __init__(self, base_roster_view: PkmRosterView):
        self._base_roster_view = base_roster_view

    @abstractmethod
    def check(self, roster: PkmRosterView, template: PkmTemplate = None) -> bool:
        pass


class RosterSizeRule(VGCRule):

    def __init__(self, base_roster_view: PkmRosterView, roster_limit=150):
        super().__init__(base_roster_view)
        self._roster_limit = roster_limit

    def check(self, roster: PkmRosterView, template: PkmTemplate = None) -> bool:
        return 0 < roster.n_pkms <= self._roster_limit


class MoveRosterSizeRule(VGCRule):

    def __init__(self, base_roster_view, move_roster_limit=150):
        super().__init__(base_roster_view)
        self._move_limit = move_roster_limit

    def check(self, roster: PkmRosterView, template: PkmTemplate = None) -> bool:
        for i in range(roster.n_pkms):
            if 0 >= roster.get_pkm_template_view(i).get_move_roster_view().n_moves > self._move_limit:
                return False
        return True


class MovesUnchangeableRule(VGCRule):

    def __init__(self, base_roster_view: PkmRosterView):
        super().__init__(base_roster_view)

    def check(self, roster: PkmRosterView, template: PkmTemplate = None) -> bool:
        return get_pkm_move_roster_view(
            template.move_roster) == self._base_roster_view.get_pkm_template_view(
            template.id).get_move_roster_view()


class TypeUnchangeableRule(VGCRule):

    def __init__(self, base_roster_view: PkmRosterView):
        super().__init__(base_roster_view)

    def check(self, roster: PkmRosterView, template: PkmTemplate = None) -> bool:
        return template.type == self._base_roster_view.get_pkm_template_view(template.id).pkm_type


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

    def check_every_rule(self, roster: PkmRoster) -> List[VGCRule]:
        failed_checks: List[VGCRule] = []
        roster_view = get_pkm_roster_view(roster)
        for rule in self._allpkm_rule_set:
            if not rule.check(roster_view):
                failed_checks.append(rule)
        for rule in self._global_rule_set:
            if not rule.check(roster_view):
                failed_checks.append(rule)
        for template, rules in self._pkm_rule_set:
            for rule in rules:
                if not rule.check(roster_view, template):
                    failed_checks.append(rule)
        return failed_checks