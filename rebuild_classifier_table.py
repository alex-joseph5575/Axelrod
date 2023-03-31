import os

from axelrod_evo import all_strategies
from axelrod_evo.classifier import all_classifiers, rebuild_classifier_table

if __name__ == "__main__":
    # Change to relative path inside axelrod_evo folder
    rebuild_classifier_table(all_classifiers, all_strategies)
