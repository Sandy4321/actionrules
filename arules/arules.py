import pandas as pd
from typing import List
import itertools
from desiredstate import DesiredState


class ActionRules:
    """
    Check all classification couples if they can make action rule
    """

    def __init__(self, stable_tables: List[pd.DataFrame], flexible_tables: List[pd.DataFrame],
                 decision_tables: List[pd.DataFrame], desired_state: DesiredState, supp: List[pd.Series],
                 conf: List[pd.Series], is_nan: bool = False):
        """
        Initialise by reduced tables.
        """
        self.stable_tables = stable_tables
        self.flexible_tables = flexible_tables
        self.decision_tables = decision_tables
        self.desired_state = desired_state
        self.action_rules = {}
        self.supp = supp
        self.conf = conf
        self.is_nan = is_nan

    def _is_action_couple(self, before, after, attribute_type):
        """
        Check if the state before and after make action rule.
        Return acton rule part and if the supp and conf can be used.
        """
        before = str(before)
        after = str(after)
        if attribute_type == "stable":
            if before == "nan" and after == "nan":
                return False, None, None
            if before == after and before != "nan":
                return True, (before,), True
            if self.is_nan:
                    if before == "nan" and after != "nan":
                        return True, (after,), False
        if attribute_type == "flexible":
            if before == "nan" and after == "nan":
                return False, None, None
            if before != after and before != "nan" and after != "nan":
                return True, (before, after), True
            if self.is_nan:
                    if before != after and before == "nan":
                        return True, (str(None), after), False
        return False, None, None

    def _create_action_rules(self, couple, attribute_type):
        action_rule_part = tuple()
        has_supp_part = True
        for column in couple:
            is_action_couple, action_couple, has_supp = self._is_action_couple(
                before=couple.at[0, column],
                after=couple.at[1, column],
                attribute_type=attribute_type)
            if is_action_couple:
                action_rule_part = action_rule_part + (column, action_couple)
                if not has_supp:
                    has_supp_part = False
        return action_rule_part, has_supp_part

    def _add_action_rule(self,
                         action_rule_stable,
                         action_rule_flexible,
                         action_rule_decision,
                         action_rule_supp,
                         action_rule_conf):
        key = (action_rule_stable, action_rule_flexible, action_rule_decision)
        if key in self.action_rules:
            action_rule_supp_used, action_rule_conf_used = self.action_rules[key]
            if (action_rule_supp[2] >= action_rule_supp_used[2] and
                    action_rule_supp[1] >= action_rule_supp_used[1] and
                    action_rule_supp[0] >= action_rule_supp_used[0]):
                self.action_rules[key] = (action_rule_supp, action_rule_conf)
        else:
            self.action_rules[key] = (action_rule_supp, action_rule_conf)

    def fit(self):
        """
        Find all couples of classification rules and try to create action rules
        """
        for table in range(len(self.stable_tables)):
            stable_columns = self.stable_tables.pop(0)
            flexible_columns = self.flexible_tables.pop(0)
            decision_column = self.decision_tables.pop(0)
            supp = self.supp.pop(0)
            conf = self.conf.pop(0)
            indexes = list(stable_columns.index.values)
            for comb in itertools.permutations(indexes, 2):
                stable_couple = stable_columns.loc[list(comb)].reset_index(drop=True)
                flexible_couple = flexible_columns.loc[list(comb)].reset_index(drop=True)
                decision_couple = decision_column.loc[list(comb)].reset_index(drop=True)
                supp_couple = supp.loc[list(comb)].reset_index(drop=True)
                conf_couple = conf.loc[list(comb)].reset_index(drop=True)
                if self.desired_state.is_candidate_couple(decision_couple):
                    action_rule_stable, has_supp_stable = self._create_action_rules(stable_couple, "stable")
                    action_rule_flexible, has_supp_flexible = self._create_action_rules(flexible_couple, "flexible")
                    action_rule_decision = (decision_couple.iat[0, 0], decision_couple.iat[1, 0])
                    if has_supp_stable and has_supp_flexible:
                        action_rule_supp = (supp_couple[0], supp_couple[1], min(supp_couple[0], supp_couple[1]))
                        action_rule_conf = (conf_couple[0], conf_couple[1], conf_couple[0] * conf_couple[1])
                    else:
                        action_rule_supp = (None, supp_couple[1], None)
                        action_rule_conf = (None, conf_couple[1], None)
                    if len(action_rule_flexible) > 0:
                        self._add_action_rule(action_rule_stable,
                                              action_rule_flexible,
                                              action_rule_decision,
                                              action_rule_supp,
                                              action_rule_conf)