import json
from typing import List, Any, Tuple

rawData = '../data/raw/fighters.json'

def get_counts(sequence):
    """
        counts items in a list

        Parameters
        ----------
        sequence: list
            a list of strings or numbers

        Returns
        -------
        list
            touples inside the list contain (element, number of occurences)
    """
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    value_key_pairs: List[Tuple[Any, int]] = [(item,count) for item,count in counts.items()]

    return value_key_pairs

#data sets


weights = [fighter['weight'] for fighter in fighters]


print(get_counts(weights))
