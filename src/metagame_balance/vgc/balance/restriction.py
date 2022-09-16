from abc import abstractmethod, ABC
from copy import deepcopy
from enum import Enum
from typing import List, Dict

from metagame_balance.vgc.datatypes.Objects import PkmTemplate, PkmRoster, PkmMoveRoster
from metagame_balance.vgc.datatypes.Types import PkmType


class RuleType(Enum):
    ROSTER_BOUNDED_SIZE = 0
    ROSTER_FIXED_SIZE = 1
    UNBANNABLE = 2
    MOVE_ROSTER_BOUNDED_SIZE = 3
    MOVE_ROSTER_FIXED_SIZE = 4
    MOVES_UNCHANGABLE = 5
    SINGLE_MOVES_UNCHANGABLE = 6
    TYPE_UNCHANGABLE = 7
    MAX_TYPE_UNCHANGABLE = 8


class DesignRule(ABC):

    @abstractmethod
    def check(self, roster: PkmRoster, template: PkmTemplate) -> bool:
        pass

    @abstractmethod
    def reason(self) -> RuleType:
        pass


class DesignConstraints(ABC):

    @abstractmethod
    def get_base_roster(self) -> PkmRoster:
        pass

    @abstractmethod
    def get_allpkm_rule_set(self) -> List[DesignRule]:
        pass

    @abstractmethod
    def get_pkm_rule_set(self, template: PkmTemplate) -> List[DesignRule]:
        pass

    @abstractmethod
    def get_global_rule_set(self) -> List[DesignRule]:
        pass

    @abstractmethod
    def check_every_rule(self, roster: PkmRoster) -> List[DesignRule]:
        pass


class VGCDesignRule(DesignRule):

    def __init__(self, base_roster: PkmRoster):
        self._base_roster = deepcopy(base_roster)

    @abstractmethod
    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        pass


""" global rules """


class RosterBoundedSizeRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, min_size=20, max_size=150):
        super().__init__(base_roster)
        self._min_size = min_size
        self._max_size = max_size

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        return self._min_size <= len(roster) <= self._max_size

    def reason(self) -> RuleType:
        return RuleType.ROSTER_BOUNDED_SIZE

    def min_size(self):
        return self._min_size

    def max_size(self):
        return self._max_size


class RosterFixedSizeRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster):
        super().__init__(base_roster)

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        return len(roster) == len(self._base_roster)

    def reason(self) -> RuleType:
        return RuleType.ROSTER_FIXED_SIZE


class UnbannableRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, template: PkmTemplate):
        super().__init__(base_roster)
        self._template = template

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        for pkm in roster:
            if pkm == self._template:
                return True
        return False

    def reason(self) -> RuleType:
        return RuleType.UNBANNABLE

    def template(self):
        return self._template


""" local rules """


class MoveRosterBoundedSizeRule(VGCDesignRule):

    def __init__(self, base_roster, max_size=20):
        super().__init__(base_roster)
        self._max_size = max_size
        self._min_size = 4
        self._template = None

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        inBounds = self._min_size <= len(template.move_roster) <= self._max_size
        if not inBounds:
            self._template = template
        return inBounds

    def reason(self) -> RuleType:
        return RuleType.MOVE_ROSTER_BOUNDED_SIZE

    def min_size(self):
        return self._min_size

    def max_size(self):
        return self._max_size

    def template(self):
        return self._template


class MoveRosterFixedSizeRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, base_move_roster: PkmMoveRoster):
        super().__init__(base_roster)
        self._base_move_roster_size = len(base_move_roster)
        self._template = None

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        equals = len(template.move_roster) == self._base_move_roster_size
        if not equals:
            self._template = template
        return equals

    def reason(self) -> RuleType:
        return RuleType.MOVE_ROSTER_FIXED_SIZE

    def base_move_roster_size(self):
        return self._base_move_roster_size


class MovesUnchangeableRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, base_move_roster: PkmMoveRoster):
        super().__init__(base_roster)
        self._base_move_roster = deepcopy(base_move_roster)
        self._template = None

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        equals = template.move_roster == self._base_move_roster
        if not equals:
            self._template = template
        return equals

    def reason(self) -> RuleType:
        return RuleType.MOVES_UNCHANGABLE

    def template(self):
        return self._template


class SingleMovesUnchangeableRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, base_move_roster: PkmMoveRoster, moves: List[bool]):
        super().__init__(base_roster)
        self._base_move_roster = deepcopy(base_move_roster)
        self._changeable_moves = moves
        self._original_move = None
        self._template = None

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        for enabled, move_original, new_move in zip(self._changeable_moves, self._base_move_roster,
                                                    template.move_roster):
            if not enabled:
                if move_original != new_move:
                    self._original_move = move_original
                    self._template = template
                    return False
        return True

    def reason(self) -> RuleType:
        return RuleType.SINGLE_MOVES_UNCHANGABLE

    def original_move(self):
        return self._original_move

    def template(self):
        return self._template


class TypeUnchangeableRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, original_type: PkmType):
        super().__init__(base_roster)
        self._original_type = original_type
        self._template = None

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        equals = template.type == self._original_type
        if not equals:
            self._template = template
        return equals

    def reason(self) -> RuleType:
        return RuleType.TYPE_UNCHANGABLE

    def original_type(self):
        return self._original_type

    def template(self):
        return self._template


class MaxHPUnchangeableRule(VGCDesignRule):

    def __init__(self, base_roster: PkmRoster, original_max_hp: float):
        super().__init__(base_roster)
        self._original_max_hp = original_max_hp
        self._template = None

    def check(self, roster: PkmRoster, template: PkmTemplate = None) -> bool:
        equals = template.max_hp == self._original_max_hp
        if not equals:
            self._template = template
        return equals

    def reason(self) -> RuleType:
        return RuleType.MAX_TYPE_UNCHANGABLE

    def original_max_hp(self):
        return self._original_max_hp

    def template(self):
        return self._template


""" design constraints data structure """


class VGCDesignConstraints(DesignConstraints):

    def __init__(self, base_roster: PkmRoster):
        self._base_roster = deepcopy(base_roster)
        self._allpkm_rule_set: List[VGCDesignRule] = []
        self._pkm_rule_set: Dict[PkmTemplate, List[VGCDesignRule]] = {}
        self._global_rule_set: List[VGCDesignRule] = []

    def get_base_roster(self) -> PkmRoster:
        return self._base_roster

    def get_allpkm_rule_set(self) -> List[DesignRule]:
        return self._allpkm_rule_set

    def add_allpkm_rule(self, rule: VGCDesignRule):
        self._allpkm_rule_set.append(rule)

    def get_pkm_rule_set(self, template: PkmTemplate) -> List[DesignRule]:
        return self._pkm_rule_set[template]

    def add_pkm_rule(self, template: PkmTemplate, rule: VGCDesignRule):
        if template not in self._pkm_rule_set:
            self._pkm_rule_set[template] = []
        self._pkm_rule_set[template].append(rule)

    def get_global_rule_set(self) -> List[DesignRule]:
        return self._global_rule_set

    def add_global_rule(self, rule: VGCDesignRule):
        self._global_rule_set.append(rule)

    def check_every_rule(self, roster: PkmRoster) -> List[VGCDesignRule]:
        failed_checks: List[VGCDesignRule] = []
        for rule in self._allpkm_rule_set:
            if not rule.check(roster):
                failed_checks.append(rule)
        for rule in self._global_rule_set:
            if not rule.check(roster):
                failed_checks.append(rule)
        for template, rules in self._pkm_rule_set.items():
            for rule in rules:
                if not rule.check(roster, template):
                    failed_checks.append(rule)
        return failed_checks
