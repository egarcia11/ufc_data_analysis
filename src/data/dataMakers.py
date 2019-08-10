import file_manager as fm
import json
import pandas as pd


class PandasMaker(object):

    fighters_path = fm.get_absolute_path('data/raw/fighters.json')
    fights_path = fm.get_absolute_path('data/raw/fights.json')

    def make_fighters(self):
        fighters = pd.DataFrame([json.loads(line) for line in open(self.fighters_path)])
        return fighters

    def make_fights(self):
        fights = pd.DataFrame([json.loads(line) for line in open(self.fights_path)])
        return fights
