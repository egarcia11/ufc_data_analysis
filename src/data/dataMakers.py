import file_manager as fm
import json
import pandas as pd

class dataMakers(object):

    dataPath = fm.get_absolute_path('data/raw/fighters.json')
    fighters = pd.DataFrame([json.loads(line) for line in open(dataPath)])

    def make(self):
        return self.fighters


    def make_weight_division(self, division):

        if division == 'strawweight':

            return 1


fightersFrame = dataMakers.make()
strawweightFrame = dataMakers.make_weight_division('strawweight')
