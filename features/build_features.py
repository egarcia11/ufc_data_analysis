import json
from typing import List, Any, Tuple

dataFile = '../data/raw/fighters.json'

fighters = [json.loads(line) for line in open(dataFile)]

weights = [fighter['weight'] for fighter in fighters]

def get_counts(sequence):

    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    value_key_pairs: List[Tuple[Any, int]] = [(item,count) for item,count in counts.items()]

    return value_key_pairs

print(get_counts(weights))
