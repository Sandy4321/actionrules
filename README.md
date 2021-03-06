# Action Rules
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Action Rules (actionrules) is an implementation of Action Rules from Classification Rules algorithm described in

```Dardzinska, A. (2013). Action rules mining. Berlin: Springer.```

## GIT repository

https://github.com/lukassykora/actionrules

## Example 1
Get data from csv.
Get action rules from classification rules. Classification rules have confidence 55% and support 3%.
Stable part of action rule is "Age".
Flexible attributes are "Embarked", "Fare", "Pclass".
Target is a Survived value 1.0.
No nan values.
Use reduction tables for speeding up.
Minimal 1 stable antecedent
Minimal 1 flexible antecedent


```python
from actionrules.actionRulesDiscovery import ActionRulesDiscovery

actionRulesDiscovery = ActionRulesDiscovery()
actionRulesDiscovery.read_csv("data/titanic.csv", sep="\t")
actionRulesDiscovery.fit(stable_antecedents = ["Age"],
                         flexible_antecedents = ["Embarked", "Fare", "Pclass"],
                         consequent = "Survived",
                         conf=55,
                         supp=3,
                         desired_classes = ["1.0"],
                         is_nan=False,
                         is_reduction=True,
                         min_stable_antecedents=1,
                         min_flexible_antecedents=1,
                         max_stable_antecedents=5,
                         max_flexible_antecedents=5)
actionRulesDiscovery.get_action_rules()
```

The output is a list where the first part is an action rule and the second part is a tuple of (support before, support after, action rule support) and (confidence before, confidence after, action rule confidence).

## Example 2
Get data from pandas dataframe.
Get action rules from classification rules. Classification rules have confidence 50% and support 3%.
Stable attributes are "Age" and "Sex".
Flexible attributes are "Embarked", "Fare", "Pclass".
Target is a Survived that changes from 0.0 to 1.0.
No nan values.
Use reduction tables for speeding up.
Minimal 1 stable antecedent
Minimal 1 flexible antecedent


```python
from actionrules.actionRulesDiscovery import ActionRulesDiscovery
import pandas as pd

dataFrame = pd.read_csv("data/titanic.csv", sep="\t")
actionRulesDiscovery = ActionRulesDiscovery()
actionRulesDiscovery.load_pandas(dataFrame)
actionRulesDiscovery.fit(stable_antecedents = ["Age", "Sex"],
                         flexible_antecedents = ["Embarked", "Fare", "Pclass"],
                         consequent = "Survived",
                         conf=50,
                         supp=3,
                         desired_changes = [["0.0", "1.0"]],
                         is_nan=False,
                         is_reduction=True,
                         min_stable_antecedents=1,
                         min_flexible_antecedents=1,
                         max_stable_antecedents=5,
                         max_flexible_antecedents=5)
actionRulesDiscovery.get_pretty_action_rules()
```

The output is a list of action rules in pretty text form.
